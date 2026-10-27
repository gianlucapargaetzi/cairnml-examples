"""Multiclass classification on CIFAR-10: a small CNN that names the object in each 32x32 colour image.

The 10 classes are airplane, automobile, bird, cat, deer, dog, frog, horse, ship and truck. The training images are
split into a training and a validation part with a fixed seed, so every run sees the same split. Loss and accuracy are
recorded for both parts after every epoch, and the trained weights are uploaded as an artifact. The data is downloaded
once into --data.
"""

import argparse
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

from cairnml import Task

CLASSES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]


def build_model() -> nn.Module:
    return nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(64 * 8 * 8, 128), nn.ReLU(), nn.Dropout(0.3),
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
    parser.add_argument("--epochs", type=int, default=10)
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
        "batch_size": args.batch_size,
        "lr": args.lr,
        "val_split": args.val_split,
        "seed": args.seed,
    })
    logger = task.get_logger()

    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    full_train = datasets.CIFAR10(args.data, train=True, download=True, transform=transforms.ToTensor())
    val_size = int(len(full_train) * args.val_split)
    train_set, val_set = random_split(
        full_train, [len(full_train) - val_size, val_size], generator=torch.Generator().manual_seed(args.seed),
    )
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=256)
    print(f"{len(train_set)} training images, {len(val_set)} validation images")

    model = build_model().to(device)
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
            logger.report_scalar("loss per step", "train", value=loss.item(), iteration=step)
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
