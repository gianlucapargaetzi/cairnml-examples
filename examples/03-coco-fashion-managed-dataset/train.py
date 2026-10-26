"""COCO Fashion through the dataset registry: the same training as example 2, read through the registry's adapter.

The registry, cairnml-dataset-registry, holds the entry for COCO Fashion: the web sources and the adapter that reads
them into the CairnML dataset format. The dataset, its revision and the registry commit are recorded on the task, so
the run shows exactly what it trained on. Example 2 trains on the same images without the registry.

Usage:
    python train.py                       # the latest registry commit
    python train.py --commit <commit>     # the registry commit of an earlier run, to rerun it exactly
"""

import argparse
from dataclasses import asdict
from itertools import islice
from pathlib import Path

from cairnml import Task
from cairnml.datasets import Dataset
from train_detector import CLASS_OF, Item, Settings, train

REGISTRY = "https://github.com/gianlucapargaetzi/cairnml-dataset-registry"
DATASET = "coco-fashion"


def items(samples, limit: int) -> list:
    """The first ``limit`` samples of a split in the registry's order (all of them if 0), as training items."""
    chosen = samples if limit == 0 else islice(samples, limit)
    out = []
    for sample in chosen:
        boxes = sample.label("bbox2d")
        out.append(Item(
            image=str(sample.modality("image")),
            boxes=[box["box"] for box in boxes],
            classes=[CLASS_OF[box["label"]] for box in boxes],
        ))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.005)
    parser.add_argument("--train-limit", type=int, default=1000, help="samples of the train split (0 for all)")
    parser.add_argument("--val-limit", type=int, default=250, help="samples of the val split (0 for all)")
    parser.add_argument("--registry", default=REGISTRY, help="URL of the dataset registry")
    parser.add_argument("--commit", default=None, help="a commit of the registry (default: the latest)")
    args = parser.parse_args()

    task = Task.init(project_name="COCO Fashion", task_name="detection with the dataset registry")
    # Reads through the adapter. This also records the dataset, its revision and the registry commit on the task.
    dataset = Dataset.get_external(DATASET, commit=args.commit, repo=args.registry, alias=DATASET)

    settings = Settings(epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
    task.connect({
        "dataset": DATASET,
        "dataset_revision": dataset.info["revision"],
        "dataset_adapter": dataset.info["adapter"],
        "registry_commit": dataset.info["repo_commit"],
        "train_limit": args.train_limit,
        "val_limit": args.val_limit,
        **asdict(settings),
    })

    train_items = items(dataset.samples("train"), args.train_limit)
    val_items = items(dataset.samples("val"), args.val_limit)
    print(f"{len(train_items)} training images, {len(val_items)} validation images")
    train(task, train_items, val_items, settings)
    task.close()


if __name__ == "__main__":
    main()
