"""CIFAR-10 classification through the dataset registry: the same training as example 2, read through the registry's adapter.

The registry, cairnml-dataset-registry, holds the entry for CIFAR-10: the publisher's archive and the adapter that reads
its batches into the CairnML dataset format. The dataset, its revision and the registry commit are recorded on the task,
so the run shows exactly what it trained on. Example 2 trains the same model without the registry.

Usage:
    python train.py                       # the latest registry commit
    python train.py --commit <commit>     # the registry commit of an earlier run, to rerun it exactly
"""

import argparse
from dataclasses import asdict

import albumentations as A
import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset, TensorDataset, random_split
from torchvision.transforms.functional import pil_to_tensor
from tqdm import tqdm

from cairnml import Task
from cairnml.datasets import Dataset as RegistryDataset

CLASSES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
REGISTRY = "https://github.com/gianlucapargaetzi/cairnml-dataset-registry"
DATASET = "cifar10"


def load_images(samples) -> TensorDataset:
    """The images and class indices of the registry's samples, as float tensors scaled to 0-1 like transforms.ToTensor."""
    samples = list(samples)
    images, labels = [], []
    for sample in tqdm(samples, desc="loading images", unit="img"):
        images.append(pil_to_tensor(Image.open(sample.modality("image")).convert("RGB")))
        labels.append(CLASSES.index(sample.label("class")))
    return TensorDataset(torch.stack(images).float() / 255, torch.tensor(labels))


def augmentation(seed: int) -> A.Compose:
    """Changes to each training image: a flip, a shift, scale and rotation, brightness and contrast, and a cut-out patch."""
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.Affine(translate_percent=0.1, scale=(0.9, 1.1), rotate=(-10, 10), p=0.6),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.CoarseDropout(num_holes_range=(1, 1), hole_height_range=(8, 8), hole_width_range=(8, 8), fill=0, p=0.3),
    ], seed=seed)


class Augmented(Dataset):
    """A dataset whose images get the transform every time they are read, so each epoch sees new variations."""

    def __init__(self, dataset: Dataset, transform: A.Compose):
        self.dataset = dataset
        self.transform = transform

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, index: int) -> tuple:
        image, label = self.dataset[index]
        image = self.transform(image=image.permute(1, 2, 0).contiguous().numpy())["image"]
        return torch.from_numpy(image).permute(2, 0, 1), label


def build_model(depth: int, dropout: float) -> nn.Module:
    """A stack of depth blocks, each with two convolutions with batch normalization, then a max-pool that halves the image.

    The channels double per block, and the model outputs logits. The saved model applies the softmax to them.
    """
    layers = []
    channels = 3
    for block in range(depth):
        out_channels = 32 * 2 ** block
        for _ in range(2):
            layers += [nn.Conv2d(channels, out_channels, kernel_size=3, padding=1), nn.BatchNorm2d(out_channels), nn.ReLU()]
            channels = out_channels
        layers += [nn.MaxPool2d(2), nn.Dropout(dropout)]
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
    for images, labels in tqdm(loader, desc="validation", leave=False):
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        total_loss += loss_function(outputs, labels).item() * len(labels)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--depth", type=int, default=3, choices=range(1, 6), help="number of blocks of two convolutions, 1 to 5")
    parser.add_argument("--dropout", type=float, default=0.1, help="dropout rate in the convolution blocks and the classifier")
    parser.add_argument("--augment", action=argparse.BooleanOptionalAction, default=True, help="augment the training images")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--val-split", type=float, default=0.1, help="fraction of the training images kept for validation")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--registry", default=REGISTRY, help="URL of the dataset registry")
    parser.add_argument("--commit", default=None, help="a commit of the registry (default: the latest)")
    args = parser.parse_args()

    task = Task.init(project_name="examples", task_name="CIFAR-10 classification with the dataset registry")
    # Reads through the adapter. This also records the dataset, its revision and the registry commit on the task.
    dataset = RegistryDataset.get_external(DATASET, commit=args.commit, repo=args.registry, alias=DATASET)
    task.connect({
        "dataset": DATASET,
        "dataset_revision": dataset.info["revision"],
        "dataset_adapter": dataset.info["adapter"],
        "registry_commit": dataset.info["repo_commit"],
        "epochs": args.epochs,
        "depth": args.depth,
        "dropout": args.dropout,
        "augment": args.augment,
        "batch_size": args.batch_size,
        "lr": args.lr,
        "val_split": args.val_split,
        "seed": args.seed,
    })
    logger = task.get_logger()

    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    full_train = load_images(dataset.samples("train"))
    val_size = int(len(full_train) * args.val_split)
    train_set, val_set = random_split(
        full_train, [len(full_train) - val_size, val_size], generator=torch.Generator().manual_seed(args.seed),
    )
    train_data = Augmented(train_set, augmentation(args.seed)) if args.augment else train_set
    train_loader = DataLoader(train_data, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=256)
    print(f"{len(train_set)} training images, {len(val_set)} validation images")

    model = build_model(args.depth, args.dropout).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    loss_function = nn.CrossEntropyLoss()

    step = 0
    for epoch in tqdm(range(args.epochs), desc="epochs", unit="epoch"):
        model.train()
        train_loss, train_correct = 0.0, 0
        for images, labels in tqdm(train_loader, desc=f"epoch {epoch + 1}", leave=False):
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
        tqdm.write(
            f"epoch {epoch + 1}/{args.epochs}: train loss {train_loss:.3f} acc {train_accuracy:.4f}, "
            f"val loss {val_loss:.3f} acc {val_accuracy:.4f}"
        )

    # The artifact is a TorchScript model that outputs class probabilities, so it loads without this file.
    probabilities = nn.Sequential(model.cpu().eval(), nn.Softmax(dim=1))
    torch.jit.script(probabilities).save("model.pt")
    task.upload_artifact("model", "model.pt")
    task.close()
    print("done: the run is in the web app, project 'examples', task 'CIFAR-10 classification with the dataset registry'")


if __name__ == "__main__":
    main()
