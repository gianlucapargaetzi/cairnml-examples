# CIFAR-10 through the dataset registry

## Goals

Train the model of [Example 2](../02-cifar10-classification) again, reading the images through the dataset registry instead of downloading them yourself.

What you will learn:

- What the dataset registry is, and when it is the easy choice.
- What a run records about a registry dataset.
- How to rerun on exactly the same data with `--commit`.

## Background

The [dataset registry](https://github.com/gianlucapargaetzi/cairnml-dataset-registry) is a library of established public datasets. Each entry is a small file that names where the data comes from, here the [Hugging Face copy](https://huggingface.co/datasets/uoft-cs/cifar10) of CIFAR-10 at a fixed commit, and an **adapter** that reads the downloaded files into one standard sample format.

You ask for a dataset by name:

```python
dataset = RegistryDataset.get_external("cifar10")
```

That replaces the download and parsing code of Example 2. The training code only sees standard samples, with named images and typed labels, whatever the files look like. Another dataset from the registry would read the same way.

**Tracking comes with the structure.** Nothing extra is needed to know what the run used: the registry commit fixes the entry and the adapter, and the run records the dataset, its source revision, the adapter and the registry commit. Pass the commit later and the same data is read the same way.

**What a registry is not.** The files stay at their source. The registry does not hold them, so a rerun needs that source to still be online. It suits public data that is easy to get again, and it is not the place for data you must be able to reproduce regardless of the internet. For that, version the data yourself, as in [Example 6](../06-regression-dataset).

## Prerequisites

- Several minutes on a CPU.
- The [SDK connected to your server](../00-installation-and-setup), with the dataset tools: `pip install "cairnml[dataset]"`.
- The prerequisites of [Example 2](../02-cifar10-classification/README.md#prerequisites). The defaults match Example 2, so the two runs can be compared.

## Steps

### 1. Install

```bash
cd examples/05-cifar-10-managed-dataset
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

In every new terminal, run `source .venv/bin/activate` again in this folder.

### 2. Run

```bash
python train.py
```

This reads the latest commit of the registry. For a quick try add `--epochs 3`.

### 3. Look at the run and compare

In the project **examples**, open the task **CIFAR-10 classification with the dataset registry**. Its **Configuration** lists the dataset `cifar10`, the dataset revision (the exact archive), the adapter and the registry commit.

Select this task and the task of Example 2 in the task list and compare them. The validation accuracy curves should be close, because only the way the data is read differs.

### 4. Rerun on the same data (optional)

Pass the registry commit from step 3:

```bash
python train.py --commit <commit>
```

## Data

[CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) by Krizhevsky. See [Example 2](../02-cifar10-classification/README.md#data) for the citation.

## Next steps

Continue with [Example 6: a regression dataset in its own repository](../06-regression-dataset).
