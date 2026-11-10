# Hyperparameter optimisation with Optuna

## Goals

Search the best learning rate, layer size and batch size for the greenhouse model, with Optuna deciding the next trial and the trials running on a queue.

What you will learn:

- How to make a training script that a search can drive, with `task.connect`.
- How to run a search with `HyperParameterOptimizer` and Optuna.
- How to compare the trials in the web app.

## Background

This example searches the best settings for a neural network. It trains a small regression model on the greenhouse dataset from [Example 6](../06-regression-dataset), and it tries many combinations of learning rate, layer size and batch size to find the one with the lowest validation error.

The search is split in two parts, and each part runs where it is cheapest:

- **Optuna** decides which settings to try next. It only does arithmetic, so it runs on the machine where you start `hpo.py`, which can be a CPU-only laptop.
- **Each trial** trains the model. Trials are sent to a queue, and an agent on that queue runs them, so they can use a GPU.

## Prerequisites

- Time: about 15 minutes on one machine, more for a full search.
- [Example 6](../06-regression-dataset) is required. It created the dataset repository. Pass its repository URL and commit to this example: `--repo` and `--commit`. The training reads that version with `Dataset.get`.
- The SDK is connected to your server, and the packages are installed (step 1).
- For the full search, an agent on a queue such as `gpu` (see step 5). You can try the whole example on one machine first with `--local`.

## Steps

### 1. Install the packages

```bash
cd examples/08-hyperparameter-optimisation
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create the base task

Run the training once with its default settings:

```bash
python train_regression.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha>
```

Pass the repository URL and the commit that Example 6 recorded. Without either one the script stops with the message `run examples/06-regression-dataset first, then pass its dataset repository URL with --repo`, or the same for `--commit`.

The script creates the task **regression baseline** in the project **examples**. It trains for 30 epochs and prints `done: validation mse ...`. Look at the task in the web app: the **Configuration** tab lists `lr`, `hidden`, `batch_size` and `epochs`, and the scalar `mse` is plotted for the training and validation sets.

Copy the **task ID** from the web app (it is in the task's details). You need it in step 4.

> **Note:** the search copies this task and changes only the hyperparameters. Every trial gets the same `repo` and `commit` as the base task, so the trials all read the same version of the dataset. See the note in step 5.

### 3. Read the search space

Open `hpo.py`. It searches three settings:

| Setting | Range | How it is sampled |
|---|---|---|
| `lr` | 0.0001 to 0.1 | on a logarithmic scale, because the right order of magnitude matters more than the exact value |
| `hidden` | 8 to 128 | any whole number |
| `batch_size` | 16, 32, 64 or 128 | one of the listed values |

Each trial runs `EPOCHS_PER_TRIAL` epochs, and the search minimises the validation `mse` at the last epoch. The search stops after `--trials` trials.

### 4. Try the search on this machine

Before you use an agent, check that everything works with a small search:

```bash
python hpo.py --base-task-id <task-id> --local --trials 4
```

`--local` runs the trials as child processes of this machine, so no agent is needed. How long four trials take depends on your machine. In the web app you will see:

- the task **hyperparameter search**, with type *optimizer*, which holds the search
- four tasks named after the base task, one per trial, each with its own settings and curves

### 5. Run the trials on a GPU agent

To use a GPU for the trials, start an agent on the GPU machine and give it a queue named `gpu` (see [step 1 of Example 4](../04-run-on-an-agent#1-start-an-agent)):

```bash
cairnml-agent daemon --queue gpu --docker --gpus 0
```

Then start the search on any machine, even one without a GPU:

```bash
python hpo.py --base-task-id <task-id> --queue gpu --trials 20 --concurrent 2
```

`--concurrent 2` runs two trials at the same time. Optuna waits for their results before it proposes the next settings, so more concurrent trials are faster but learn a little less from each result.

**Data for the trials.** An agent reads the dataset by the URL and commit that the base task holds, the same way your machine does. Each trial copies those values from the base task, and reads the commit with `Dataset.get`. The repository is private, so the CairnML GitHub App must be installed on it (Example 6, step 6), and the server gives the job read access to it.

### 6. Compare the results

Open the task **hyperparameter search**. The web app shows the objective of every trial, and the trial with the lowest validation `mse` is listed first. The script also prints the three best trials at the end of a run:

```
top trial 3f9c...: regression baseline
```

Open one of them and look at:

- **Configuration:** the settings this trial used
- **Scalars:** the `mse` curves for the training and validation sets

Compare the learning rates of the best and the worst trials. A very high learning rate makes the curve jump around, and a very small one may not finish learning within 30 epochs. Check this in your own results.

## Data

The data is generated by [Example 6](../06-regression-dataset). It is synthetic and carries no license restrictions.

## Next steps

Continue with [Example 9: reports and plots](../09-reports-and-plots), which shows what you can record next to the scalars.
