# CIFAR-10 through the dataset registry

This example trains the same model as [Example 2](../02-cifar10-classification), with the same settings on the same images. The difference is where the data comes from: the [dataset registry](https://github.com/gianlucapargaetzi/cairnml-dataset-registry). The registry has an entry for CIFAR-10 that points to its [Hugging Face copy](https://huggingface.co/datasets/uoft-cs/cifar10), pinned to a commit, and an adapter that reads its Parquet files into the CairnML dataset format.

## Features

- Reads the data through the registry's adapter, so the training code only sees standard samples.
- Records the dataset, its revision, the adapter and the registry commit on the run.
- Reruns an earlier run exactly, from the registry commit it used.
- Trains on the same images as Example 2, so the two runs can be compared.
- Shows a progress bar for the image loading, the epochs and the batches.

## Prerequisites

- The [SDK connected to your server](../../README.md#prerequisites), with the dataset tools: `pip install "cairnml[dataset]"`
- The prerequisites of [Example 2](../02-cifar10-classification/README.md#prerequisites)

## Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python train.py
```

The script reads the latest commit of the registry. To rerun an earlier run exactly, pass the registry commit it recorded:

```bash
python train.py --commit <commit>
```

The defaults match Example 2: 80 epochs, batch size 32, three blocks, dropout 0.1, augmentation on and a 10% validation split.

## What to look for

The run is in the project **examples**, task **CIFAR-10 classification with the dataset registry**. Its configuration lists:

- the dataset, `cifar10`
- the dataset revision, which identifies the exact archive
- the adapter that read it
- the registry commit

Compare its validation accuracy curve with the run of Example 2.

## Data

The data is [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) by Krizhevsky. See [Example 2](../02-cifar10-classification/README.md#data) for the citation.

## Next steps

Continue with [Run on an agent](../10-run-on-an-agent), which sends a run to a machine running `cairnml-agent`.
