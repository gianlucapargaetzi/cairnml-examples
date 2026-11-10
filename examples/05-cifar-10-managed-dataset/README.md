# CIFAR-10 through the dataset registry

## Goals

Train the model of [Example 2](../02-cifar10-classification) on the same images, but read the data through the **dataset registry**, so the run records exactly which dataset version it used.

What you will learn:

- How a public dataset is read with `RegistryDataset.get_external`, and what a run records about it.
- How to rerun an earlier run on exactly the same data, with `--commit`.
- How to compare this run with the run of Example 2.

## Background

The [dataset registry](https://github.com/gianlucapargaetzi/cairnml-dataset-registry) has an entry for CIFAR-10 that points to its [Hugging Face copy](https://huggingface.co/datasets/uoft-cs/cifar10), pinned to a commit, and an adapter that reads its Parquet files into the CairnML dataset format.

What the example does:

- The training code sees standard samples, whatever the source format.
- The run records the dataset, its revision, the adapter and the registry commit.
- The defaults match Example 2: 40 epochs, batch size 32, three blocks, dropout 0.1, augmentation on and a 10% validation split.

## Before you start

- Time: several minutes on a CPU.
- The [SDK connected to your server](../00-installation-and-setup), with the dataset tools: `pip install "cairnml[dataset]"`.
- The prerequisites of [Example 2](../02-cifar10-classification/README.md#before-you-start).

## Steps

### 1. Install

```bash
cd examples/05-cifar-10-managed-dataset
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run

```bash
python train.py
```

The script reads the latest commit of the registry. For a quick try, add `--epochs 3`.

### 3. Rerun on the same data (optional)

Pass the registry commit that an earlier run recorded:

```bash
python train.py --commit <commit>
```

## What to look for

You end with a task whose configuration names the dataset, its revision and the registry commit.

The run is in the project **examples**, task **CIFAR-10 classification with the dataset registry**. Its **Configuration** lists:

- the dataset, `cifar10`
- the dataset revision, which identifies the exact archive
- the adapter that read it
- the registry commit

Select this task and the task of Example 2 in the list and **compare** them: the validation accuracy curves should be close.

## Data

The data is [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) by Krizhevsky. See [Example 2](../02-cifar10-classification/README.md#data) for the citation.

## Next steps

Continue with [Example 6: a regression dataset in its own repository](../06-regression-dataset).
