# CIFAR-10 classification

This example trains a small convolutional network to name the object in a 32x32 colour photograph: airplane, automobile, bird, cat, deer, dog, frog, horse, ship or truck. It is a multiclass classification task, unlike the detection in [Example 3](../03-coco-fashion-detection), which also finds where each object is. The data is downloaded once, and every step and every epoch is recorded on your server.

## Features

- Downloads CIFAR-10 once from Hugging Face, about 120 MB.
- Holds out 10% of the training images as a validation set, with a fixed seed, so every run uses the same split.
- Augments the training images with a flip, a shift, scale and rotation, brightness and contrast changes, and a cut-out patch. Use `--no-augment` to turn this off. The validation images are never augmented.
- Trains a small CNN with settings you can change on the command line.
- Records the loss of every step, and the loss and accuracy of the training and validation sets after every epoch.
- Uploads the trained weights as an artifact.

## Prerequisites

- The [SDK connected to your server](../../README.md#prerequisites)
- A GPU is optional. The example runs on a CPU in several minutes.

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

The defaults train for 40 epochs with batch size 64, four convolution blocks, dropout 0.3 and augmentation on. To change them:

```bash
python train.py --epochs 20 --batch-size 128 --lr 0.001 --depth 3 --dropout 0.4
```

`--depth` sets the number of convolution blocks, from 1 to 5. Each block halves the image, so a depth of 5 reduces the 32x32 image to 1x1.

## What to look for

The run is in the project **CIFAR-10**, task **multiclass classification**:

- The loss per step, for the training set.
- The loss and accuracy per epoch, for the training and validation sets.
- The trained weights under artifacts, as `model`.

## Data

The data is [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) by Krizhevsky, collected from the 80 Million Tiny Images dataset. The training images are downloaded from its [Hugging Face copy](https://huggingface.co/datasets/uoft-cs/cifar10), which is faster to download than the original archive. Please cite it when you use it:

> Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, 2009. [Technical report](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf)

## Next steps

Continue with [Example 3: COCO Fashion detection](../03-coco-fashion-detection), which trains a detector on garments in real photographs with bounding boxes.
