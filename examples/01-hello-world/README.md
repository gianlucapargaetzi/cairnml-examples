# Hello world

## Goals

Record your first run on your server, and see which lines of code make a script a tracked run.

What you will learn:

- That `Task.init` is what turns a script into a task on the server.
- How to record settings with `task.connect`, and why they are kept apart from the code.
- How to log a curve with `report_scalar` and upload a file as an artifact.
- How to compare runs in the web app, and how to tell a changed setting from a changed line of code.

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

- About 3 minutes.
- The [SDK connected to your server](../00-installation-and-setup).

## Steps

### 1. Install

From the root of the repository:

```bash
source .venv/bin/activate
cd examples/01-hello-world
pip install -r requirements.txt
```

In every new terminal, go to the repository root and run `source .venv/bin/activate` again.

### 2. Run

```bash
python hello_world.py
```

The script finishes in a few seconds. It adds a small random noise to the curve, so two runs differ. Pass `--seed 7` to repeat a run exactly.

### 3. Look at the run

While the script runs, the task is listed as **Running** with a small progress bar: the `tqdm` bar `steps` is found automatically, nothing is logged for it. In the web app open the project **examples**, task **hello world**:

- **Configuration:** the settings `greeting`, `steps` and `seed`.
- **Scalars:** the `loss` curve, one point per step.
- **Artifacts:** `hello.txt`.

Run the script again and compare the two experiments: only the noise differs.

### 4. Change the seed and the code

One more run shows the difference between a setting and a line of code. In `hello_world.py`, make the noise ten times larger by changing `0.01` to `0.1`:

```python
loss = 1.0 / (step + 1) + rng.gauss(0.0, 0.1)
```

Do not commit the change. Run the script with any seed you like:

```bash
python hello_world.py --seed 7
```

Select the new task and the first run in the task list, click **Compare** and look for the differences:

- **Scalars:** the new curve is much more jagged.
- **Configuration:** the `seed` is now `7`. It explains a different noise, but not a jagged one.
- **Execution:** open the new task and find **Uncommitted changes**. It shows your edit to `hello_world.py` as a diff, with `0.01` replaced by `0.1`. The first run has no such diff.

> [!IMPORTANT]
> The SDK reads the changes from the git repository that the script sits in, here the one you cloned in Example 0. That is why **Uncommitted changes** shows up.

This is what a recorded run is for. The settings explain what you chose to expose, and **Execution** keeps the code that ran, including changes you never committed. Try another change, such as `steps` or the `greeting`, and find it again in **Configuration**, **Scalars** or **Artifacts**.

When you are done, undo the edit so that the next examples start from the original script:

```bash
git checkout hello_world.py
```

> [!CAUTION]
> We use git here only to get through this example. `git checkout hello_world.py` throws away every uncommitted change in that file, which is what we want here. Do not run it on work you want to keep.

## Troubleshooting

- **The script cannot connect:** run `cairnml init http://<server-ip>` again, and check that the web app opens at that address.

## Next steps

Continue with [Example 2: CIFAR-10 classification](../02-cifar10-classification).
