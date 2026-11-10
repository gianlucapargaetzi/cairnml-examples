# CIFAR-10 classification

## Goals

Train a real model, a small convolutional network that names the object in a photograph, and see its loss and accuracy curves in the web app.

What you will learn:

- How a full training script is tracked: settings, curves and the trained model.
- How training and validation curves are recorded per epoch.
- How a script can send itself to an agent with `--queue` (used in Example 4).

## Background

CIFAR-10 has 32x32 colour photographs of ten classes: airplane, automobile, bird, cat, deer, dog, frog, horse, ship and truck. This is a multiclass classification task. [Example 3](../03-private-code-and-credentials) takes this same code into a private repository, and [Example 4](../04-run-on-an-agent) runs it on an agent.

What the example does:

- Downloads CIFAR-10 once from Hugging Face, about 120 MB, into `cifar10/`.
- Holds out 10% of the training images as a validation set, with a fixed seed, so every run uses the same split.
- Augments the training images with a flip, a shift, scale and rotation, brightness and contrast changes, and a cut-out patch. `--no-augment` turns this off. The validation images are never augmented.
- Records the loss and accuracy of the training and validation sets after every epoch, and uploads the trained weights as an artifact.
- Shows progress bars for the download, the image loading, the epochs and the batches.

## Before you start

- Time: several minutes on a CPU, much less on a GPU.
- The [SDK connected to your server](../00-installation-and-setup).
- Optional: a GPU. Install the PyTorch build for your CUDA version first if the default one does not match it. See [pytorch.org](https://pytorch.org).

## Steps

### 1. Install

```bash
cd examples/02-cifar10-classification
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run

```bash
python train.py
```

The defaults are 40 epochs, batch size 32, three blocks, dropout 0.1, learning rate 0.001, augmentation on and a 10% validation split. To change them:

```bash
python train.py --epochs 20 --batch-size 128 --lr 0.001 --depth 4 --dropout 0.3
```

| Option | Meaning |
|---|---|
| `--depth` | number of blocks, 1 to 5. Each block has two convolutions with batch normalization and halves the image, so depth 5 reduces 32x32 to 1x1 |
| `--seed` | seed of the split, the weights and the augmentation |
| `--queue <name>` | queue the run for an agent instead of training here. See [Example 4](../04-run-on-an-agent) |

For a quick try, add `--epochs 3`.

## What to look for

You end with one task, **CIFAR-10 classification**, with curves and the trained model.

The run is in the project **examples**, task **CIFAR-10 classification**:

- **Scalars:** `loss` and `accuracy`, each with a `train` and a `val` series, one point per epoch. The validation curve shows whether the model overfits: a training loss that keeps falling while the validation loss rises.
- **Configuration:** the settings of the run.
- **Artifacts:** the trained model, `model`. It is a TorchScript model that takes 32x32 colour images with values from 0 to 1 and outputs class probabilities that sum to 1. Load it with `torch.jit.load("model.pt")`.

## Data

The data is [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) by Krizhevsky, collected from the 80 Million Tiny Images dataset. The training images are downloaded from its [Hugging Face copy](https://huggingface.co/datasets/uoft-cs/cifar10), which is faster than the original archive. Please cite it when you use it:

> Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, 2009. [Technical report](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf)

## Next steps

Continue with [Example 3: private code and credentials](../03-private-code-and-credentials), which moves this training into a private repository.
