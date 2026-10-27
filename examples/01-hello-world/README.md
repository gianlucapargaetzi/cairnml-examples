# Hello world

The smallest possible CairnML run: one task with parameters, a loss curve and an artifact, recorded on your server. Use it to check that the SDK is connected before you run anything bigger.

## Features

- Records a run's parameters with `task.connect`.
- Logs a metric curve with `report_scalar`.
- Uploads a file as an artifact.

## Prerequisites

- The [SDK connected to your server](../../README.md#prerequisites)

## Run

```bash
python hello_world.py
```

The script finishes in a few seconds and prints the name of the run.

## What to look for

Open the web app and go to the project **examples**, task **hello world**:

- The parameters are listed in the task's configuration.
- The `loss` curve, one point per step, is under scalars.
- `hello.txt` is listed under artifacts.

## Next steps

Continue with [Example 2: CIFAR-10 classification](../02-cifar10-classification).
