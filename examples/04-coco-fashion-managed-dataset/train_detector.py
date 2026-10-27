"""Fine-tune a COCO-pretrained Faster R-CNN (MobileNetV3-FPN) on COCO Fashion, reporting to CairnML.

The model, the settings and the evaluation are the same in every COCO Fashion example. Only where the images come
from differs, so each example hands ``train`` a list of ``Item`` objects.
"""

import io
from dataclasses import dataclass
from typing import List, Sequence, Tuple, Union

import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchmetrics.detection import MeanAveragePrecision
from torchvision.models.detection import FasterRCNN_MobileNet_V3_Large_FPN_Weights, fasterrcnn_mobilenet_v3_large_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.transforms.functional import to_tensor

# The 46 Fashionpedia categories, in the order of their ids. Class 0 is the background.
CATEGORIES = [
    "shirt, blouse", "top, t-shirt, sweatshirt", "sweater", "cardigan", "jacket", "vest", "pants", "shorts",
    "skirt", "coat", "dress", "jumpsuit", "cape", "glasses", "hat", "headband, head covering, hair accessory",
    "tie", "glove", "watch", "belt", "leg warmer", "tights, stockings", "sock", "shoe", "bag, wallet", "scarf",
    "umbrella", "hood", "collar", "lapel", "epaulette", "sleeve", "pocket", "neckline", "buckle", "zipper",
    "applique", "bead", "bow", "flower", "fringe", "ribbon", "rivet", "ruffle", "sequin", "tassel",
]
CLASS_OF = {name: index + 1 for index, name in enumerate(CATEGORIES)}


@dataclass
class Item:
    """One image: its bytes or a path, its boxes as [x1, y1, x2, y2] in pixels, and its class ids."""

    image: Union[bytes, str]
    boxes: List[Sequence[float]]
    classes: List[int]


@dataclass
class Settings:
    epochs: int = 3
    batch_size: int = 4
    lr: float = 0.005
    max_size: int = 1024
    min_size: int = 640
    workers: int = 4


class Detection(Dataset):
    def __init__(self, items: List[Item]):
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int):
        item = self.items[index]
        source = io.BytesIO(item.image) if isinstance(item.image, bytes) else item.image
        image = to_tensor(Image.open(source).convert("RGB"))
        target = {
            "boxes": torch.tensor(item.boxes, dtype=torch.float32).reshape(-1, 4),
            "labels": torch.tensor(item.classes, dtype=torch.int64),
        }
        return image, target


def collate(batch: List[Tuple[torch.Tensor, dict]]):
    return tuple(zip(*batch))


def build_model(settings: Settings):
    model = fasterrcnn_mobilenet_v3_large_fpn(
        weights=FasterRCNN_MobileNet_V3_Large_FPN_Weights.COCO_V1,
        min_size=settings.min_size,
        max_size=settings.max_size,
    )
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, len(CATEGORIES) + 1)
    return model


@torch.no_grad()
def evaluate(model, items: List[Item], device, batch_size: int) -> float:
    """Mean average precision over IoU 0.50:0.95 of the validation items."""
    metric = MeanAveragePrecision(box_format="xyxy", iou_type="bbox")
    model.eval()
    loader = DataLoader(Detection(items), batch_size=batch_size, collate_fn=collate)
    for images, targets in loader:
        outputs = model([image.to(device) for image in images])
        metric.update(
            [{k: v.cpu() for k, v in out.items()} for out in outputs],
            [{k: v.cpu() for k, v in target.items()} for target in targets],
        )
    return float(metric.compute()["map"])


def train(task, train_items: List[Item], val_items: List[Item], settings: Settings) -> None:
    """Train on train_items, report the loss of every step and the validation mAP of every epoch."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger = task.get_logger()
    model = build_model(settings).to(device)
    loader = DataLoader(
        Detection(train_items), batch_size=settings.batch_size, shuffle=True,
        num_workers=settings.workers, collate_fn=collate,
    )
    optimizer = torch.optim.SGD(
        [p for p in model.parameters() if p.requires_grad], lr=settings.lr, momentum=0.9, weight_decay=1e-4,
    )
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=max(1, settings.epochs - 1), gamma=0.1)

    step = 0
    for epoch in range(settings.epochs):
        model.train()
        for images, targets in loader:
            images = [image.to(device) for image in images]
            targets = [{k: v.to(device) for k, v in target.items()} for target in targets]
            loss = sum(model(images, targets).values())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            logger.report_scalar("loss", "train", value=loss.item(), iteration=step)
            step += 1
        scheduler.step()
        map_value = evaluate(model, val_items, device, settings.batch_size)
        logger.report_scalar("mAP", "val", value=map_value, iteration=epoch)
        print(f"epoch {epoch + 1}/{settings.epochs}: loss {loss.item():.3f}, val mAP {map_value:.4f}")

    torch.save(model.state_dict(), "model.pt")
    task.upload_artifact("model", "model.pt")
