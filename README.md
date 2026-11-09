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

# 🧭 CairnML Examples

> 🎯 **Goal:** learn what the CairnML platform does by running small, guided examples on your own server. Each one records its run there, and the examples build on each other.

Start with the setup, then the hello world, train a real model, put the code in a **private** repository, run it on an **agent**, then move on to datasets, workflows, searches, reports and imports.

## ✨ Features

- A setup guide (example 0) and eleven runnable examples, from a single tracked run to a hyperparameter search.
- A full path for **private code**: a private GitHub repository, a GitHub App, a credential in CairnML, and a run on an agent that reads the repository.
- Runs appear in the web app, with their parameters, metrics, loss curves and artifacts.
- Datasets are versioned: a run records the repository, the commit and the content hash of the data it read.
- Every README has the same shape: a **Goal**, what you will learn, what you need, numbered steps, what to look for, and what comes next.

## ✅ Prerequisites

- A running [CairnML server](https://github.com/gianlucapargaetzi/cairnml-server) and Python 3.9 or newer.
- An account, the web app, the SDK and an enrolled machine: [Example 0](examples/00-installation-and-setup) guides you through all of it.
- A [GitHub](https://github.com) account for examples 3 to 6, and [git](https://git-scm.com). The GitHub command line `gh` is **optional**: every step that can use it also shows the way in the browser.

## 🗺️ Examples

| | Example | What it shows |
|---|---|---|
| 🧰 | [Installation and setup](examples/00-installation-and-setup) | An account, the first sign-in, a tour of the web app, the terminology, the SDK and enrolling your machine |
| 👋 | [Hello world](examples/01-hello-world) | One run with parameters, a metric curve and an artifact |
| 🖼️ | [CIFAR-10 classification](examples/02-cifar10-classification) | Multiclass classification of small photographs, with curves and the trained model |
| 🔐 | [Private code and credentials](examples/03-private-code-and-credentials) | A private repository, a GitHub App, and the credential that lets CairnML read it |
| 🤖 | [Run on an agent](examples/04-run-on-an-agent) | Running the private code on an agent, from the command line and from the web app |
| 🗂️ | [CIFAR-10 through the dataset registry](examples/05-cifar-10-managed-dataset) | The same training as example 2, reading the data through the dataset registry |
| 🌱 | [A regression dataset in its own repository](examples/06-regression-dataset) | Generating a dataset from a seed, publishing it as a private dataset repository, and reading it through the SDK |
| 🔀 | [A workflow of three steps](examples/07-workflow-pipeline) | Preparing data, training and evaluating as one pipeline, with each step as its own task |
| 🎛️ | [Hyperparameter optimisation with Optuna](examples/08-hyperparameter-optimisation) | A search over learning rate, layer size and batch size, with the trials on a queue |
| 📊 | [Reports and plots](examples/09-reports-and-plots) | Scatter plots, histograms, tables, confusion matrices and images next to the scalars |
| ♻️ | [The life of a task](examples/10-task-lifecycle) | Cloning, queueing, archiving, moving, publishing and deleting a task |
| 📥 | [Import a run from a project that does not use CairnML](examples/11-import-external-run) | Adapting a legacy training folder to CairnML's import format and uploading it |

Each example has its own README with the steps, the command to run and what to look for in the web app. Examples 6 to 11 need the dataset repository that example 6 creates.

## ⚖️ Compare the runs

Examples 2 and 5 use the same model, settings and images. After both have run, open the **examples** project in the web app and compare the two tasks. Their validation accuracy curves should be close, and the configuration of the run of example 5 shows the dataset, its revision and the registry commit.

## 🆘 Having problems

1. Check the [open issues](https://github.com/gianlucapargaetzi/cairnml-examples/issues).
2. If your problem is not listed, [open a new issue](https://github.com/gianlucapargaetzi/cairnml-examples/issues/new) with the example you ran, the command, and the full error message.
