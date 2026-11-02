"""Train the greenhouse model of Example 4, then report what it got right and wrong in six different ways.

Scalars (one number per step) are only part of a run. This script also records:

    a scatter plot       predicted against actual energy, for the test set
    a histogram          the residuals, which are actual minus predicted energy
    a table              the mean absolute error for each hour of the day
    a confusion matrix   "expensive hour" yes or no, from the predictions
    an image             a figure saved with matplotlib: residuals against outside temperature
    a text               a short summary, shown in the Console tab

    python reports.py --repo <clone>                # the default settings, 30 epochs
    python reports.py --repo <url> --commit <sha>   # another version of the dataset, read with the SDK

Run Example 4 first, then pass its dataset repository with --repo (a URL or the local clone).
--commit is the version to read (default: the HEAD of the local clone).
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", help="the dataset repository: a URL, or a local clone")
    parser.add_argument("--commit", help="the commit of the dataset (default: the HEAD of the local clone)")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--hidden", type=int, default=32)
    args = parser.parse_args()
    if args.repo is None:
        parser.error("run examples/04-regression-dataset first, then pass its dataset repository with --repo")
    if args.commit is None:
        args.commit = subprocess.run(
            ["git", "-C", args.repo, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    return args


def train(x_train, y_train, x_test, y_test, epochs: int, lr: float, hidden: int, logger) -> nn.Module:
    """Train the network for the given epochs. Each epoch is one step on the scalar curves."""
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(len(FEATURES), hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(),
                          nn.Linear(hidden, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_function = nn.MSELoss()
    for epoch in range(epochs):
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
            logger.report_scalar("mse", "train", value=loss_function(model(x_train), y_train).item(), iteration=epoch)
            logger.report_scalar("mse", "test", value=loss_function(model(x_test), y_test).item(), iteration=epoch)
    return model


def report_scatter(logger, actual: np.ndarray, predicted: np.ndarray) -> None:
    """The first 300 test points, as (actual, predicted). A perfect model puts every point on the diagonal."""
    points = list(zip(actual[:300].tolist(), predicted[:300].tolist()))
    logger.report_scatter2d(
        "predictions", "test", scatter=points, iteration=0,
        xaxis="actual energy (kWh)", yaxis="predicted energy (kWh)", mode="markers",
    )


def report_residuals(logger, residuals: np.ndarray) -> None:
    """The residuals of all test rows. A good model has residuals centred on zero, with no pattern."""
    logger.report_histogram(
        "residuals", "test", values=residuals.tolist(), iteration=0,
        xaxis="actual minus predicted (kWh)", yaxis="count",
    )


def report_hourly_error(logger, frame: pd.DataFrame) -> None:
    """The mean absolute error for each hour of the day, as a table. Hours with a larger error are where the model is weakest."""
    table = frame.groupby("hour")["absolute_error"].mean().round(3).reset_index()
    table.columns = ["hour", "mean absolute error (kWh)"]
    logger.report_table("error by hour", "test", iteration=0, table_plot=table)


def report_expensive_hours(logger, actual: np.ndarray, predicted: np.ndarray) -> None:
    """A yes or no question from the energy numbers: is this hour expensive, meaning above the median? The confusion matrix
    counts how often the model's answer matches the truth. Rows are the truth, columns are the model's answer."""
    threshold = np.median(actual)
    truth = actual > threshold
    answer = predicted > threshold
    matrix = np.array([
        [np.sum(~truth & ~answer), np.sum(~truth & answer)],
        [np.sum(truth & ~answer), np.sum(truth & answer)],
    ])
    logger.report_confusion_matrix(
        "expensive hour", "test", matrix=matrix, iteration=0,
        xaxis="model answer", yaxis="truth", xlabels=["cheap", "expensive"], ylabels=["cheap", "expensive"],
    )


def report_figure(logger, frame: pd.DataFrame, path: Path) -> None:
    """A figure made with matplotlib and saved as a PNG file, then uploaded. Use it for anything the other reports
    cannot show, for example a plot with a custom layout."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axis = plt.subplots(figsize=(7, 4.5))
    scatter = axis.scatter(frame["outside_temp"], frame["residual"], c=frame["hour"], cmap="viridis", s=8)
    axis.axhline(0, color="black", linewidth=0.8)
    axis.set_xlabel("outside temperature (°C)")
    axis.set_ylabel("residual (kWh)")
    axis.set_title("residuals by outside temperature, colour = hour of day")
    fig.colorbar(scatter, ax=axis, label="hour")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    logger.report_image("residuals vs temperature", "test", iteration=0, local_path=str(path))


def main() -> None:
    args = parse_args()
    task = Task.init(project_name="examples", task_name="reports and plots")
    settings = task.connect({
        "epochs": args.epochs, "lr": args.lr, "hidden": args.hidden, "repo": args.repo, "commit": args.commit,
    })
    logger = task.get_logger()

    # Dataset.get downloads the version once and records it on this task, so the run shows which data it used.
    data = Dataset.get(settings["repo"], settings["commit"])
    train_frame = pd.read_csv(data.path / "train.csv")
    test_frame = pd.read_csv(data.path / "test.csv")
    mean, spread = train_frame[FEATURES].mean(), train_frame[FEATURES].std()
    x_train = torch.tensor(((train_frame[FEATURES] - mean) / spread).values, dtype=torch.float32)
    y_train = torch.tensor(train_frame[TARGET].values, dtype=torch.float32).unsqueeze(1)
    x_test = torch.tensor(((test_frame[FEATURES] - mean) / spread).values, dtype=torch.float32)
    y_test = torch.tensor(test_frame[TARGET].values, dtype=torch.float32).unsqueeze(1)

    model = train(x_train, y_train, x_test, y_test, settings["epochs"], settings["lr"], settings["hidden"], logger)
    model.eval()
    with torch.no_grad():
        predicted = model(x_test).squeeze(1).numpy()
    actual = test_frame[TARGET].values
    residuals = actual - predicted

    results = test_frame.copy()
    results["predicted"] = predicted
    results["residual"] = residuals
    results["absolute_error"] = np.abs(residuals)

    report_scatter(logger, actual, predicted)
    report_residuals(logger, residuals)
    report_hourly_error(logger, results)
    report_expensive_hours(logger, actual, predicted)
    report_figure(logger, results, Path("residuals.png"))

    summary = (
        f"Test set: {len(results)} rows. Mean absolute error {np.abs(residuals).mean():.3f} kWh. "
        f"Mean residual {residuals.mean():+.3f} kWh (close to zero means no systematic bias)."
    )
    logger.report_text(summary)
    task.close()
    print("done: the reports are in the web app, project 'examples', task 'reports and plots'")


if __name__ == "__main__":
    main()
