<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/cairnml-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/cairnml-logo.svg">
    <img src="assets/cairnml-logo.svg" alt="CairnML" width="480">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/gianlucapargaetzi/cairnml-examples/stargazers"><img src="https://img.shields.io/github/stars/gianlucapargaetzi/cairnml-examples?style=flat-square&logo=github" alt="GitHub stars"></a>
</p>

# CairnML Examples

Guided examples of what the CairnML platform can do. Each example runs on your own server and records its run there. The examples build on each other: start with the hello world, then the CIFAR-10 classification, then the two COCO Fashion examples, which train the same detector on the same images in two different ways.

## Features

- Four runnable examples, from a single tracked run to a full training run.
- Runs appear in the web app, with their parameters, metrics, loss curves and artifacts.
- The fourth example reads its data through the dataset registry, so the run records which dataset and revision it used.
- Examples 3 and 4 train on the same images, so their runs can be compared side by side.

## Prerequisites

- Python 3.9 or newer
- The [SDK](https://github.com/gianlucapargaetzi/cairnml) connected to a running [CairnML server](https://github.com/gianlucapargaetzi/cairnml-server):

```bash
pip install cairnml
cairnml init http://<server-ip>
```

`<server-ip>` is the address of the server, with a port only if the server does not use port 80. The command works out the rest.

## Examples

| Example | What it shows |
|---|---|
| [Hello world](examples/01-hello-world) | One run with parameters, a metric curve and an artifact |
| [CIFAR-10 classification](examples/02-cifar10-classification) | Multiclass classification of small photographs, with a loss curve and test accuracy |
| [COCO Fashion detection](examples/03-coco-fashion-detection) | Training a detector on downloaded data, without a registry |
| [COCO Fashion through the dataset registry](examples/04-coco-fashion-managed-dataset) | The same training, reading the data through the dataset registry |

Each example has its own README with the installation steps, the command to run and what to look for in the web app.

## Compare the runs

Examples 3 and 4 use the same model, settings and images. After both have run, open the **COCO Fashion** project in the web app and compare the two tasks. Their validation mAP curves should be close, and the configuration of the fourth run shows the dataset, its revision and the registry commit.

## Having problems

1. Check the [open issues](https://github.com/gianlucapargaetzi/cairnml-examples/issues).
2. If your problem is not listed, [open a new issue](https://github.com/gianlucapargaetzi/cairnml-examples/issues/new) with the example you ran, the command, and the full error message.
