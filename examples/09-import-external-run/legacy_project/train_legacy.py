"""A training script from a project that does not use CairnML: it writes its own files and knows nothing about CairnML.

It trains a small network on the greenhouse dataset of Example 4 and writes one folder per run:

    runs/<name>_<timestamp>/
        settings.txt        the settings, one "name = value" per line
        log.csv             one row per epoch, with its own column names
        model_final.pth     the weights after the last epoch (a PyTorch state dict)
        model_best.pth      the weights of the epoch with the best validation loss

The file names and the column names are this project's own. The export script in ../export_to_cairnml.py turns such a
folder into the layout CairnML imports.

    python train_legacy.py --epochs 20
    python train_legacy.py --data $(cairnml dataset get <repository> <commit>)   # another version of the dataset

--data is the folder with train.csv and test.csv. By default it is the data/ folder of the clone that Example 4 created.
"""

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd
import torch
from torch import nn

FEATURES = ["outside_temp", "light", "humidity", "co2", "hour"]
TARGET = "energy"
DEFAULT_DATA = Path(__file__).resolve().parent.parent.parent / "greenhouse-data" / "data"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--hidden", type=int, default=16)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--out", type=Path, default=Path("runs"))
    args = parser.parse_args()

    torch.manual_seed(0)
    train = pd.read_csv(args.data / "train.csv")
    test = pd.read_csv(args.data / "test.csv")
    mean, spread = train[FEATURES].mean(), train[FEATURES].std()
    x_train = torch.tensor(((train[FEATURES] - mean) / spread).values, dtype=torch.float32)
    y_train = torch.tensor(train[TARGET].values, dtype=torch.float32).unsqueeze(1)
    x_test = torch.tensor(((test[FEATURES] - mean) / spread).values, dtype=torch.float32)
    y_test = torch.tensor(test[TARGET].values, dtype=torch.float32).unsqueeze(1)

    model = nn.Sequential(nn.Linear(len(FEATURES), args.hidden), nn.ReLU(), nn.Linear(args.hidden, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    loss_function = nn.MSELoss()

    run = args.out / f"greenhouse_mlp_{datetime.now():%Y%m%d_%H%M%S}"
    run.mkdir(parents=True)
    (run / "settings.txt").write_text(
        f"data folder = {args.data}\nepochs = {args.epochs}\nlearning rate = {args.lr}\nhidden units = {args.hidden}\n"
        f"batch size = {args.batch_size}\n"
    )

    rows, best = [], float("inf")
    for epoch in range(1, args.epochs + 1):
        model.train()
        order = torch.randperm(len(x_train))
        for start in range(0, len(order), args.batch_size):
            batch = order[start:start + args.batch_size]
            loss = loss_function(model(x_train[batch]), y_train[batch])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_loss = loss_function(model(x_test), y_test).item()
            predictions = model(x_test)
            ss_res = ((y_test - predictions) ** 2).sum().item()
            ss_tot = ((y_test - y_test.mean()) ** 2).sum().item()
        with torch.no_grad():
            train_loss = loss_function(model(x_train), y_train).item()
        rows.append({"Epoch": epoch, "Train Loss": round(train_loss, 5), "Val Loss": round(val_loss, 5),
                     "Val R2": round(1 - ss_res / ss_tot, 5)})
        if val_loss < best:
            best = val_loss
            torch.save(model.state_dict(), run / "model_best.pth")

    pd.DataFrame(rows).to_csv(run / "log.csv", index=False)
    torch.save(model.state_dict(), run / "model_final.pth")
    print(f"run written to {run}: best validation loss {best:.4f}, final R2 {rows[-1]['Val R2']}")


if __name__ == "__main__":
    main()
