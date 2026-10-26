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

Guided examples of what the CairnML platform can do. Each one builds on the last.

## 🧰 Prerequisites

- 🐍 Python 3.9 or newer
- 🖥️ A running [CairnML server](https://github.com/gianlucapargaetzi/cairnml-server), and the [SDK](https://github.com/gianlucapargaetzi/cairnml) connected to it:

```bash
pip install cairnml
cairnml-init --server http://<server-ip>:8008
```

## 📚 Examples

| # | Example | What you learn |
|---|---|---|
| 1 | [🌍 Hello world](examples/01-hello-world) | Track a run: parameters, metrics and an artifact |
| 2 | [👗 COCO Fashion detection](examples/02-coco-fashion-detection) | Train a detector on a public dataset, tracked as a run |
| 3 | [🗂️ COCO Fashion, managed dataset](examples/03-coco-fashion-managed-dataset) | The same training on a versioned dataset, recorded on the run |

Example 2 and 3 train the same model on the same images. Compare their runs in the web app to see what the managed dataset adds.

## 🆘 Having problems

1. Check the [open issues](https://github.com/gianlucapargaetzi/cairnml-examples/issues).
2. If your problem is not listed, [open a new issue](https://github.com/gianlucapargaetzi/cairnml-examples/issues/new) with the example you ran and the full error message.
