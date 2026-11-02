"""A workflow of three steps on the greenhouse dataset: prepare the data, train a model, evaluate it.

Each function marked as a component runs as its own task in CairnML, with its own log, parameters and outputs. The
function that is marked as the pipeline connects them: it decides the order and passes the outputs of one step to the
next. The steps only import what they use inside their own bodies, because CairnML runs each of them on its own.

    python pipeline.py --local                # the whole workflow on this machine, each step as a sub-process task
    python pipeline.py --repo https://github.com/<you>/greenhouse-data.git --commit <sha>
                                              # each step is queued on DEFAULT_QUEUE, and an agent runs it

The dataset is the greenhouse dataset of Example 4. By default it is the clone that Example 4 created, at its HEAD commit.
An agent cannot read a folder on your machine, so for the queued run pass the repository URL and a commit.
"""

import argparse
import subprocess
from pathlib import Path

from cairnml.automation import PipelineDecorator

PROJECT = "examples"
# The queue whose agents run the steps. Use a queue with a GPU agent to train on the GPU.
DEFAULT_QUEUE = "default"
# The dataset repository that Example 4 created next to it: a local clone, read at its HEAD commit by default.
DEFAULT_REPO = str(Path(__file__).resolve().parent.parent / "greenhouse-data")


@PipelineDecorator.component(return_values=["data_dir"], execution_queue=DEFAULT_QUEUE)
def prepare_data(dataset_repo: str, dataset_commit: str) -> str:
    """Read the dataset version with the SDK. The files are downloaded once into the cache, and the run records the
    repository, the commit and the content hash."""
    from cairnml.datasets import Dataset

    data = Dataset.get(dataset_repo, dataset_commit)
    return str(data.path)


@PipelineDecorator.component(return_values=["model_path", "val_mse"], execution_queue=DEFAULT_QUEUE)
def train(data_dir: str, lr: float, hidden: int, epochs: int):
    """Train a small network and save its weights. The return values are the path of the file and the last validation
    mean squared error."""
    import torch
    import pandas as pd
    from torch import nn

    features = ["outside_temp", "light", "humidity", "co2", "hour"]
    target = "energy"
    train_frame = pd.read_csv(f"{data_dir}/train.csv")
    test_frame = pd.read_csv(f"{data_dir}/test.csv")
    mean, spread = train_frame[features].mean(), train_frame[features].std()

    def tensors(frame):
        x = torch.tensor(((frame[features] - mean) / spread).values, dtype=torch.float32)
        y = torch.tensor(frame[target].values, dtype=torch.float32).unsqueeze(1)
        return x, y

    x_train, y_train = tensors(train_frame)
    x_test, y_test = tensors(test_frame)
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(len(features), hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(),
                          nn.Linear(hidden, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_function = nn.MSELoss()
    for _ in range(epochs):
        model.train()
        order = torch.randperm(len(x_train))
        for start in range(0, len(order), 64):
            batch = order[start:start + 64]
            loss = loss_function(model(x_train[batch]), y_train[batch])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        val_mse = loss_function(model(x_test), y_test).item()
    model_path = "model.pth"
    torch.save(model.state_dict(), model_path)
    return model_path, val_mse


@PipelineDecorator.component(return_values=["test_r2"], execution_queue=DEFAULT_QUEUE)
def evaluate(data_dir: str, model_path: str) -> float:
    """Load the saved weights and score them on the test file with the R² score: 1.0 is a perfect fit."""
    import torch
    import pandas as pd
    from torch import nn

    features = ["outside_temp", "light", "humidity", "co2", "hour"]
    target = "energy"
    train_frame = pd.read_csv(f"{data_dir}/train.csv")
    test_frame = pd.read_csv(f"{data_dir}/test.csv")
    mean, spread = train_frame[features].mean(), train_frame[features].std()
    x = torch.tensor(((test_frame[features] - mean) / spread).values, dtype=torch.float32)
    y = torch.tensor(test_frame[target].values, dtype=torch.float32).unsqueeze(1)

    hidden = torch.load(model_path, weights_only=True)["0.weight"].shape[0]
    model = nn.Sequential(nn.Linear(len(features), hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(),
                          nn.Linear(hidden, 1))
    model.load_state_dict(torch.load(model_path, weights_only=True))
    model.eval()
    with torch.no_grad():
        predictions = model(x)
        ss_res = ((y - predictions) ** 2).sum().item()
        ss_tot = ((y - y.mean()) ** 2).sum().item()
    return 1 - ss_res / ss_tot


@PipelineDecorator.pipeline(name="greenhouse workflow", project=PROJECT, version="1.0", default_queue=DEFAULT_QUEUE)
def run_workflow(dataset_repo: str, dataset_commit: str, lr: float = 0.01, hidden: int = 32, epochs: int = 30) -> None:
    data_dir = prepare_data(dataset_repo, dataset_commit)
    model_path, val_mse = train(data_dir, lr, hidden, epochs)
    test_r2 = evaluate(data_dir, model_path)
    print(f"workflow done: validation mse {float(val_mse):.4f}, test R2 {float(test_r2):.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local", action="store_true", help="run every step on this machine")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="the dataset repository: a URL, or a local clone")
    parser.add_argument("--commit", help="the commit of the dataset (default: the HEAD of the local clone)")
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--hidden", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=30)
    args = parser.parse_args()
    commit = args.commit or subprocess.run(
        ["git", "-C", args.repo, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()

    if args.local:
        PipelineDecorator.run_locally()
    run_workflow(dataset_repo=args.repo, dataset_commit=commit, lr=args.lr, hidden=args.hidden, epochs=args.epochs)


if __name__ == "__main__":
    main()
