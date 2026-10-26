# 👗 COCO Fashion detection

Trains a fashion detector: a COCO-pretrained Faster R-CNN (MobileNetV3-FPN) fine-tuned on 46 garment and accessory classes. Every step and epoch is tracked on your server. The data is downloaded from the dataset's own web sources and read directly, with no registry and no dataset management. [Example 3](../03-coco-fashion-managed-dataset) trains the same model on the same images through the dataset registry.

## 🧰 Prerequisites

- The [SDK connected to your server](../../README.md#-prerequisites)
- A GPU helps a lot. The example also runs on a CPU, slowly.
- About 4 GB of disk space and a download of the same size, once

## 📦 Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Install the PyTorch build for your CUDA version first if the default one does not match your GPU. See [pytorch.org](https://pytorch.org).

## 🚀 Run

```bash
python train.py
```

The defaults train for 3 epochs on the first 1,000 training images and validate on the first 250 validation images, in the order of the annotation files. Change them with `--epochs`, `--train-limit` and `--val-limit`, for example `python train.py --epochs 1 --train-limit 40 --val-limit 20` for a quick check. `--train-limit 0` uses every training image.

## 👀 See it

The run is in project **COCO Fashion**, task **detection without dataset management**: the loss per step, the validation mAP per epoch, and the trained weights under artifacts (`model`).

## 📄 Data

[Fashionpedia](https://fashionpedia.github.io), in COCO format, licensed CC BY 4.0. Please cite it when you use the data:

> Jia et al., *Fashionpedia: Ontology, Segmentation, and an Attribute Localization Dataset*, ECCV 2020. [arXiv:2004.12276](https://arxiv.org/abs/2004.12276)

## ➡️ Next

[Example 3: COCO Fashion through the dataset registry](../03-coco-fashion-managed-dataset)
