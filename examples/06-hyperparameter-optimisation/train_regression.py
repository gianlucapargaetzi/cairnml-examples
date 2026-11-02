"""Train a small neural network on the greenhouse dataset of example 4: the base run for the hyperparameter search.

Run it once by hand to create the base task. The search (hpo.py) copies this task for every trial and changes the
hyperparameters, so the values here are only the starting point.

    python train_regression.py                 # one run with the default hyperparameters
    python train_regression.py --lr 0.003      # another run, to try a value yourself

The dataset is read with the SDK: --repo is the dataset repository and --commit its version. By default they are the
clone that Example 4 created, at its HEAD commit. The agents of the search cannot read a folder on your machine, so
give them the URL of the repository and the commit, with --repo and --commit, when you create the base task.

The script uses the GPU when there is one. The search does not need it: only the trials run this script.
"""

import argparse
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn

from cairnml import Task
from cairnml.datasets import Dataset

FEATURES = ["outside_temp", "light", "humidity", "co2", "hour"]
TARGET = "energy"
# The dataset repository that Example 4 created next to it.
DEFAULT_REPO = str(Path(__file__).resolve().parent.parent / "greenhouse-data")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=DEFAULT_REPO, help="the dataset repository: a URL, or a local clone")
    parser.add_argument("--commit", help="the commit of the dataset (default: the HEAD of the local clone)")
    parser.add_argument("--lr", type=float, default=0.01, help="learning rate of the Adam optimizer")
    parser.add_argument("--hidden", type=int, default=32, help="number of units in each hidden layer")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.commit is None:
        args.commit = subprocess.run(
            ["git", "-C", args.repo, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    return args


def load(folder: Path):
    """The training and validation tensors. The features are scaled with the mean and spread of the training data only,
    so the validation data never leaks into the scaling."""
    train = pd.read_csv(folder / "train.csv")
    test = pd.read_csv(folder / "test.csv")
    mean, spread = train[FEATURES].mean(), train[FEATURES].std()
    to_tensors = lambda frame: (
        torch.tensor(((frame[FEATURES] - mean) / spread).values, dtype=torch.float32),
        torch.tensor(frame[TARGET].values, dtype=torch.float32).unsqueeze(1),
    )
    return to_tensors(train), to_tensors(test)


def build(hidden: int) -> nn.Module:
    return nn.Sequential(
        nn.Linear(len(FEATURES), hidden), nn.ReLU(),
        nn.Linear(hidden, hidden), nn.ReLU(),
        nn.Linear(hidden, 1),
    )


def main() -> None:
    args = parse_args()
    task = Task.init(project_name="examples", task_name="regression baseline")
    # The search changes these values on the trial tasks. connect returns what the task actually uses.
    settings = task.connect({
        "lr": args.lr,
        "hidden": args.hidden,
        "batch_size": args.batch_size,
        "epochs": args.epochs,
        "seed": args.seed,
        "repo": args.repo,
        "commit": args.commit,
    })

    # Dataset.get downloads the version once and records it on this task, so the run shows which data it used.
    data = Dataset.get(settings["repo"], settings["commit"])
    torch.manual_seed(settings["seed"])
    np.random.seed(settings["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    (x_train, y_train), (x_val, y_val) = load(data.path)
    x_train, y_train, x_val, y_val = (t.to(device) for t in (x_train, y_train, x_val, y_val))

    model = build(settings["hidden"]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=settings["lr"])
    loss_function = nn.MSELoss()
    logger = task.get_logger()

    for epoch in range(settings["epochs"]):
        model.train()
        order = torch.randperm(len(x_train), device=device)
        for start in range(0, len(order), settings["batch_size"]):
            batch = order[start:start + settings["batch_size"]]
            loss = loss_function(model(x_train[batch]), y_train[batch])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            train_mse = loss_function(model(x_train), y_train).item()
            val_mse = loss_function(model(x_val), y_val).item()
        # "mse" / "val" is the objective of the search: the search minimises the last value of this scalar.
        logger.report_scalar("mse", "train", value=train_mse, iteration=epoch)
        logger.report_scalar("mse", "val", value=val_mse, iteration=epoch)

    print(f"done: validation mse {val_mse:.4f} on {device}")
    task.close()


if __name__ == "__main__":
    main()
