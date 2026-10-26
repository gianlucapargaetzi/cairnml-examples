# 🗂️ COCO Fashion through the dataset registry

The same detector and settings as [Example 2](../02-coco-fashion-detection), trained on the same images. The difference is where the data comes from: the dataset registry. [cairnml-dataset-registry](https://github.com/gianlucapargaetzi/cairnml-dataset-registry) holds the entry for COCO Fashion, which points to its web sources, and the adapter that reads them into the CairnML dataset format. The run records the dataset, its revision and the registry commit, so you can see later exactly what the model was trained on.

## 🧰 Prerequisites

- The [SDK connected to your server](../../README.md#-prerequisites), with the dataset tools: `pip install "cairnml[dataset]"`
- Everything that Example 2 needs, see its [prerequisites](../02-coco-fashion-detection/README.md#-prerequisites)

## 📦 Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Run

```bash
python train.py
```

To rerun an earlier run exactly, pass the registry commit it used:

```bash
python train.py --commit <commit>
```

## 👀 See it

The run is in project **COCO Fashion**, task **detection with the dataset registry**. Its configuration lists the dataset, the adapter, the dataset revision and the registry commit.

## 📄 Data

Fashionpedia, CC BY 4.0. See [Example 2](../02-coco-fashion-detection/README.md#-data) for the citation.
