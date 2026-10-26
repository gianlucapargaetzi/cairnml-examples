# COCO Fashion through the dataset registry

This example trains the same model as [Example 2](../02-coco-fashion-detection), with the same settings on the same images. The difference is where the data comes from: the [dataset registry](https://github.com/gianlucapargaetzi/cairnml-dataset-registry). The registry has an entry for COCO Fashion that points to its web sources, and an adapter that reads them into the CairnML dataset format.

## Features

- Reads the data through the registry's adapter, so the training code only sees standard samples.
- Records the dataset, its revision, the adapter and the registry commit on the run.
- Reruns an earlier run exactly, from the registry commit it used.
- Trains on the same images as Example 2, so the two runs can be compared.

## Prerequisites

- The [SDK connected to your server](../../README.md#prerequisites), with the dataset tools: `pip install "cairnml[dataset]"`
- The prerequisites of [Example 2](../02-coco-fashion-detection/README.md#prerequisites)

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

The defaults match Example 2: 3 epochs on the first 1,000 training samples and 250 validation samples.

## What to look for

The run is in the project **COCO Fashion**, task **detection with the dataset registry**. Its configuration lists:

- the dataset, `coco-fashion`
- the dataset revision, which identifies the exact web source files
- the adapter that read them
- the registry commit

Compare its validation mAP curve with the run of Example 2.

## Data

The data is Fashionpedia, licensed under CC BY 4.0. See [Example 2](../02-coco-fashion-detection/README.md#data) for the citation.
