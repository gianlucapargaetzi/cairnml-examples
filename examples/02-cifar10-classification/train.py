"""Multiclass classification on CIFAR-10: a small CNN that names the object in each 32x32 colour image.

The 10 classes are airplane, automobile, bird, cat, deer, dog, frog, horse, ship and truck. The training images are
split into a training and a validation part with a fixed seed, so every run sees the same split. Loss and accuracy are
recorded for both parts after every epoch, and the trained weights are uploaded as an artifact. The data is downloaded
once into --data.
"""

import argparse
import io
import urllib.request
from pathlib import Path

import pyarrow.parquet as pq
import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split
from torchvision.transforms.functional import pil_to_tensor

from cairnml import Task

CLASSES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
HF_BASE = "https://huggingface.co/datasets/uoft-cs/cifar10/resolve/main/plain_text"
TRAIN_FILE = "train-00000-of-00001.parquet"


def download(data: Path) -> Path:
    """The training images as a parquet file in --data, downloaded from Hugging Face once."""
    target = data / TRAIN_FILE
    if not target.exists():
        data.mkdir(parents=True, exist_ok=True)
        print(f"downloading {TRAIN_FILE} ...")
        partial = target.with_suffix(".part")
        urllib.request.urlretrieve(f"{HF_BASE}/{TRAIN_FILE}", partial)
        partial.rename(target)
    return target


def load_images(path: Path) -> TensorDataset:
    """The PNG images and labels of a parquet file, as float tensors scaled to 0-1 like transforms.ToTensor."""
    table = pq.read_table(path).to_pydict()
    images = torch.stack([pil_to_tensor(Image.open(io.BytesIO(item["bytes"])).convert("RGB")) for item in table["img"]])
    return TensorDataset(images.float() / 255, torch.tensor(table["label"]))


def build_model(depth: int, dropout: float) -> nn.Module:
    """A stack of depth convolution blocks, each halving the image, then a classifier. The channels double per block."""
    layers = []
    channels = 3
    for block in range(depth):
        out_channels = 32 * 2 ** block
        layers += [nn.Conv2d(channels, out_channels, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Dropout2d(dropout)]
        channels = out_channels
    side = 32 // 2 ** depth
    return nn.Sequential(
        *layers,
        nn.Flatten(),
        nn.Linear(channels * side * side, 128), nn.ReLU(), nn.Dropout(dropout),
        nn.Linear(128, len(CLASSES)),
    )


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, device: torch.device, loss_function) -> tuple:
    """The mean loss and the accuracy of the model on a loader."""
    model.eval()
    total_loss, correct = 0.0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        total_loss += loss_function(outputs, labels).item() * len(labels)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--depth", type=int, default=2, choices=range(1, 6), help="number of convolution blocks, 1 to 5")
    parser.add_argument("--dropout", type=float, default=0.3, help="dropout rate in the convolution blocks and the classifier")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--val-split", type=float, default=0.1, help="fraction of the training images kept for validation")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--data", type=Path, default=Path("cifar10"))
    args = parser.parse_args()

    task = Task.init(project_name="CIFAR-10", task_name="multiclass classification")
    task.connect({
        "dataset": "CIFAR-10",
        "epochs": args.epochs,
        "depth": args.depth,
        "dropout": args.dropout,
        "batch_size": args.batch_size,
        "lr": args.lr,
        "val_split": args.val_split,
        "seed": args.seed,
    })
    logger = task.get_logger()

    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    full_train = load_images(download(args.data))
    val_size = int(len(full_train) * args.val_split)
    train_set, val_set = random_split(
        full_train, [len(full_train) - val_size, val_size], generator=torch.Generator().manual_seed(args.seed),
    )
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=256)
    print(f"{len(train_set)} training images, {len(val_set)} validation images")

    model = build_model(args.depth, args.dropout).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    loss_function = nn.CrossEntropyLoss()

    step = 0
    for epoch in range(args.epochs):
        model.train()
        train_loss, train_correct = 0.0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = loss_function(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # logger.report_scalar("loss per step", "train", value=loss.item(), iteration=step)
            step += 1
            train_loss += loss.item() * len(labels)
            train_correct += (outputs.argmax(dim=1) == labels).sum().item()

        train_loss /= len(train_set)
        train_accuracy = train_correct / len(train_set)
        val_loss, val_accuracy = evaluate(model, val_loader, device, loss_function)
        logger.report_scalar("loss", "train", value=train_loss, iteration=epoch)
        logger.report_scalar("loss", "val", value=val_loss, iteration=epoch)
        logger.report_scalar("accuracy", "train", value=train_accuracy, iteration=epoch)
        logger.report_scalar("accuracy", "val", value=val_accuracy, iteration=epoch)
        print(
            f"epoch {epoch + 1}/{args.epochs}: train loss {train_loss:.3f} acc {train_accuracy:.4f}, "
            f"val loss {val_loss:.3f} acc {val_accuracy:.4f}"
        )

    torch.save(model.state_dict(), "model.pt")
    task.upload_artifact("model", "model.pt")
    task.close()
    print("done: the run is in the web app, project 'CIFAR-10', task 'multiclass classification'")


if __name__ == "__main__":
    main()
