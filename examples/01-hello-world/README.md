# Hello world

## Goals

Record your first run on your server, and see which lines of code make a script a tracked run.

What you will learn:

- That `Task.init` is what turns a script into a task on the server.
- How to record settings with `task.connect`, and why they are kept apart from the code.
- How to log a curve with `report_scalar` and upload a file as an artifact.

## Background

The script has four SDK calls. Everything else is ordinary Python:

```python
task = Task.init(project_name="examples", task_name="hello world")    # registers the run on the server
settings = task.connect({"greeting": "Hello, CairnML!", "steps": 10}) # records the settings
logger.report_scalar(title="loss", series="train", value=loss, iteration=step)  # one point of a curve
task.upload_artifact("hello", artifact_object="hello.txt")            # stores a file with the run
```

Settings go through `task.connect` so that the server knows them. A copy of the task can then start with other values without anyone editing the code, as [Example 4](../04-run-on-an-agent) shows.

## Prerequisites

- Under a minute.
- The [SDK connected to your server](../00-installation-and-setup).

## Steps

### 1. Install

```bash
cd examples/01-hello-world
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

In every new terminal, run `source .venv/bin/activate` again in this folder.

### 2. Run

```bash
python hello_world.py
```

The script finishes in a few seconds. It adds a small random noise to the curve, so two runs differ. Pass `--seed 7` to repeat a run exactly.

### 3. Look at the run

In the web app open the project **examples**, task **hello world**:

- **Configuration:** the settings `greeting`, `steps` and `seed`.
- **Scalars:** the `loss` curve, one point per step.
- **Artifacts:** `hello.txt`.

Run the script again and compare the two experiments: only the noise differs.

## Troubleshooting

- **The script cannot connect:** run `cairnml init http://<server-ip>` again, and check that the web app opens at that address.

## Next steps

Continue with [Example 2: CIFAR-10 classification](../02-cifar10-classification).
