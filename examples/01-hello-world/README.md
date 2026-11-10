# Hello world

## Goals

Record your first run on your server and check that the SDK is connected, before you run anything bigger.

What you will learn:

- How a script becomes a run: `Task.init`.
- How to record parameters with `task.connect`.
- How to log a metric curve with `report_scalar`, and upload a file as an artifact.

## Background

The smallest possible CairnML run: one task with parameters, a loss curve and an artifact.

## Prerequisites

- Time: under a minute.
- The [SDK connected to your server](../00-installation-and-setup).

## Steps

### 1. Install

```bash
cd examples/01-hello-world
pip install -r requirements.txt
```

### 2. Run

```bash
python hello_world.py
```

The script finishes in a few seconds and prints the seed it used and the name of the run. The seed makes the small noise on the curve: pass `--seed 7` to repeat a run exactly, or leave it out to get a different curve each time.

### 3. Look at the run

Open the web app, project **examples**, task **hello world**:

- **Configuration:** the parameters `greeting`, `steps` and `seed`.
- **Scalars:** the `loss` curve, one point per step, and the `seed`.
- **Artifacts:** `hello.txt`.

Run it twice and compare the two tasks: only the noise on the curve differs.

## Troubleshooting

- **The script cannot connect:** run `cairnml init http://<server-ip>` again, and check that the web app opens at that address.

## Next steps

Continue with [Example 2: CIFAR-10 classification](../02-cifar10-classification).
