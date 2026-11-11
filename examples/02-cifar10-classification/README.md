# CIFAR-10 classification

## Goals

Train a small convolutional network on CIFAR-10 and follow its training in the web app.

What you will learn:

- How a full training script is tracked: its settings, one curve point per epoch, and the trained model.
- How to read the training and validation curves, and how they show overfitting.
- How the web app shows how far a running training is, without any logging in the script.

## Background

CIFAR-10 is 60,000 colour photographs of 32x32 pixels in ten classes: airplane, automobile, bird, cat, deer, dog, frog, horse, ship and truck. The network learns to name the object in a photograph.

Two choices in the script matter for what you will see:

- **A validation set.** 10% of the training images are held out, with a fixed seed, so every run uses the same split. The model never trains on them. A model that keeps improving on the training images but not on these is memorising, not learning.
- **Augmentation.** The training images are randomly flipped, shifted, scaled, rotated, brightened and partly covered, so the model sees a slightly different picture each epoch and generalises better. The validation images are never altered. `--no-augment` turns it off.

- **Progress.** The script logs no progress. It uses `tqdm` bars for the download, the loading of the images and the epochs, and for the batches of each epoch. The SDK finds them, so the web app shows a running task with a bar. The bar of the epochs is the progress of the run, with the batches of the current epoch below it. `Task.init(..., progress_bar="epochs")` names that bar, so that the download and the loading of the images do not count as training. A loop without `tqdm` can use `Task.progress(iterable, label="epochs")` instead.

This is the code that [Example 3](../03-private-code-and-credentials) moves into a private repository and [Example 4](../04-run-on-an-agent) runs on an agent.

## Prerequisites

- Several minutes on a CPU, much less on a GPU.
- The [SDK connected to your server](../00-installation-and-setup).
- Optional: a GPU. Install the PyTorch build for your CUDA version first if the default one does not match it. See [pytorch.org](https://pytorch.org).

## Steps

### 1. Install

From the root of the repository:

```bash
source .venv/bin/activate
cd examples/02-cifar10-classification
pip install -r requirements.txt
```

In every new terminal, go to the repository root and run `source .venv/bin/activate` again.

### 2. Run

```bash
python train.py
```

The images, about 120 MB, are downloaded once into `cifar10/`. The defaults are 40 epochs, batch size 32, three blocks, dropout 0.1 and learning rate 0.001. For a quick try add `--epochs 3`. To change the settings:

```bash
python train.py --epochs 20 --batch-size 128 --lr 0.001 --depth 4 --dropout 0.3
```

| Option | Meaning |
|---|---|
| `--depth` | Number of blocks, 1 to 5. Each block has two convolutions and halves the image, so depth 5 reduces 32x32 to 1x1 |
| `--seed` | Seed of the split, the weights and the augmentation |
| `--queue <name>` | Queue the run for an agent instead of training here ([Example 4](../04-run-on-an-agent)) |

### 3. Look at the run

While it trains, the project **examples** lists the task **CIFAR-10 classification** as **Running** with a small bar and the percentage. While the images load, the bar moves along without a percentage, because that is not the epochs. Open the task to see the bar of the epochs with the batches of the current epoch below it.

When it has finished, look at the task:

- **Scalars:** `loss` and `accuracy`, each with a `train` and a `val` series, one point per epoch. If the training loss keeps falling while the validation loss rises, the model overfits.
- **Configuration:** the settings of the run.
- **Artifacts:** the trained model, a TorchScript file that takes 32x32 colour images with values from 0 to 1 and returns class probabilities. Load it with `torch.jit.load("model.pt")`.

> [!NOTE]
> Worth a try once the first run is done: `python train.py --no-augment`. Compare the two runs and see how augmentation changes the gap between the training and the validation curves.

## Data

[CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) by Krizhevsky, downloaded from its [Hugging Face copy](https://huggingface.co/datasets/uoft-cs/cifar10), which is faster than the original archive. Please cite it when you use it:

> Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, 2009. [Technical report](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf)

## Next steps

Continue with [Example 3: private code and credentials](../03-private-code-and-credentials).
