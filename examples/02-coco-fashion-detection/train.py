"""COCO Fashion without dataset management: download the web sources, read them and train.

The annotations and images come straight from the project's download page, unpacked into --cache. Nothing is
registered or versioned, and the run records no dataset. Example 3 trains the same model on the same images, read
through the dataset registry.

Fashionpedia is CC BY 4.0. Cite: Jia et al., "Fashionpedia: Ontology, Segmentation, and an Attribute
Localization Dataset", ECCV 2020 (arXiv:2004.12276).
"""

import argparse
import json
import urllib.request
import zipfile
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

from cairnml import Task
from train_detector import CLASS_OF, Item, Settings, train

BASE = "https://s3.amazonaws.com/ifashionist-dataset"
# split: (annotation file, archive, folder of the images inside the archive's unpacked folder)
SOURCES = {
    "train": ("annotations/instances_attributes_train2020.json", "images/train2020.zip", "train2020/train"),
    "val": ("annotations/instances_attributes_val2020.json", "images/val_test2020.zip", "val_test2020/test"),
}


def download(url: str, target: Path) -> Path:
    if not target.exists():
        print(f"downloading {url} ...")
        urllib.request.urlretrieve(url, target)
    return target


def fetch(split: str, cache: Path):
    """The annotation file of a split, and the folder its images are in (the archive is unpacked once)."""
    cache.mkdir(parents=True, exist_ok=True)
    annotations, archive, folder = SOURCES[split]
    annotation_file = download(f"{BASE}/{annotations}", cache / Path(annotations).name)
    unpacked = cache / Path(archive).stem
    if not unpacked.exists():
        zip_file = download(f"{BASE}/{archive}", cache / Path(archive).name)
        with zipfile.ZipFile(zip_file) as handle:
            handle.extractall(unpacked)
        zip_file.unlink()
    return annotation_file, cache / folder


def items(split: str, cache: Path, limit: int):
    """The first ``limit`` images of a split in annotation order (all of them if 0), as training items."""
    annotation_file, image_folder = fetch(split, cache)
    data = json.loads(annotation_file.read_text())
    names = {category["id"]: category["name"] for category in data["categories"]}
    boxes = defaultdict(list)
    for ann in data["annotations"]:
        x, y, width, height = ann["bbox"]
        if width <= 0 or height <= 0:  # the same empty boxes the registry adapter skips
            continue
        boxes[ann["image_id"]].append(([x, y, x + width, y + height], CLASS_OF[names[ann["category_id"]]]))
    images = data["images"] if limit == 0 else data["images"][:limit]
    return [
        Item(
            image=str(image_folder / image["file_name"]),
            boxes=[box for box, _ in boxes[image["id"]]],
            classes=[cls for _, cls in boxes[image["id"]]],
        )
        for image in images
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.005)
    parser.add_argument("--train-limit", type=int, default=1000, help="images of the train split (0 for all)")
    parser.add_argument("--val-limit", type=int, default=250, help="images of the val split (0 for all)")
    parser.add_argument("--cache", type=Path, default=Path("coco-fashion-web"))
    args = parser.parse_args()

    task = Task.init(project_name="COCO Fashion", task_name="detection without dataset management")
    settings = Settings(epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
    task.connect({
        "dataset": "COCO Fashion web sources (not managed)",
        "train_limit": args.train_limit,
        "val_limit": args.val_limit,
        **asdict(settings),
    })

    train_items = items("train", args.cache, args.train_limit)
    val_items = items("val", args.cache, args.val_limit)
    print(f"{len(train_items)} training images, {len(val_items)} validation images")
    train(task, train_items, val_items, settings)
    task.close()


if __name__ == "__main__":
    main()
