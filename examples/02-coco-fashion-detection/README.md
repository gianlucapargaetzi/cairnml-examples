# COCO Fashion detection

This example trains a fashion detector: a COCO-pretrained Faster R-CNN with a MobileNetV3 backbone, fine-tuned on 46 garment and accessory classes from the Fashionpedia dataset. The data is downloaded from the dataset's own web sources and read directly, without a registry and without dataset management. Every step and every epoch is recorded on your server.

## Features

- Downloads the COCO-format annotations and images of the official web sources, once.
- Fine-tunes a detector pretrained on COCO, with settings you can change on the command line.
- Records the loss of every step and the validation mAP of every epoch.
- Uploads the trained weights as an artifact.

## Prerequisites

- The [SDK connected to your server](../../README.md#prerequisites)
- A GPU helps a lot. The example also runs on a CPU, but slowly.
- About 4 GB of free disk space, and the same amount of download the first time

## Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Install the PyTorch build for your CUDA version first if the default one does not match your GPU. See [pytorch.org](https://pytorch.org).

## Run

```bash
python train.py
```

The defaults train for 3 epochs on the first 1,000 training images and validate on the first 250 validation images, in the order of the annotation files. For a quick check, run a smaller version:

```bash
python train.py --epochs 1 --train-limit 40 --val-limit 20
```

`--train-limit 0` uses every training image.

## What to look for

The run is in the project **COCO Fashion**, task **detection without dataset management**:

- The loss curve, one point per step.
- The validation mAP curve, one point per epoch.
- The trained weights under artifacts, as `model`.

## Data

The data is [Fashionpedia](https://fashionpedia.github.io) in COCO format, licensed under CC BY 4.0. Please cite it when you use it:

> Jia et al., *Fashionpedia: Ontology, Segmentation, and an Attribute Localization Dataset*, ECCV 2020. [arXiv:2004.12276](https://arxiv.org/abs/2004.12276)

## Next steps

Continue with [Example 3: COCO Fashion through the dataset registry](../03-coco-fashion-managed-dataset), which trains the same model on the same images.
