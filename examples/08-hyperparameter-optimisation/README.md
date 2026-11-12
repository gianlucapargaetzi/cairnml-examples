# Hyperparameter optimisation with Optuna

## Goals

Search the best learning rate, layer size and batch size for the greenhouse model, with Optuna proposing the settings and the trials running as tasks of their own.

What you will learn:

- Why a training script must expose its settings with `task.connect` for a search to drive it.
- How `HyperParameterOptimizer` and Optuna run a search.
- How to compare the trials in the web app.

## Background

A model has settings the training does not learn, such as the learning rate. They change the result a lot, and trying them by hand is slow. A **search** automates it: it proposes values, trains with them, reads the validation error, and proposes better values.

Two parts do the work, each where it is cheapest:

- **Optuna** proposes the next values from the results so far. It only does arithmetic, so it runs where you start `hpo.py`, even on a laptop without a GPU.
- **Each trial** trains the model. It is a copy of a **base task** with new values, so it is an ordinary task you can open and compare. Trials go to a queue, and an agent there runs them, which is where a GPU helps.

The copy works because the base task records its settings with `task.connect`: the search overrides those values and nothing in the code. Every trial also inherits the dataset repository and commit of the base task, so all trials read the same data.

## Prerequisites

- About 15 minutes on one machine, more for a full search.
- [Example 6](../06-regression-dataset) done. Its repository URL and commit are passed as `--repo` and `--commit`.
- The [SDK connected to your server](../00-installation-and-setup).
- For a search on an agent, an agent as in [Example 4](../04-run-on-an-agent). You can try everything on one machine first with `--local`.

## Steps

### 1. Install

From the root of the repository:

```bash
source .venv/bin/activate
cd examples/08-hyperparameter-optimisation
pip install -r requirements.txt
```

In every new terminal, go to the repository root and run `source .venv/bin/activate` again.

### 2. Create the base task

Run the training once with its default settings:

```bash
python train_regression.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha>
```

This creates the task **regression baseline** in the project **examples**. It trains for 30 epochs and prints `done: validation mse ...`. Its **Configuration** lists `lr`, `hidden`, `batch_size` and `epochs`, and its `mse` curve shows the training and validation error.

Copy the task ID from the task's details. The search needs it.

### 3. Read the search space

`hpo.py` searches three settings:

| Setting | Range | Sampled |
|---|---|---|
| `lr` | 0.0001 to 0.1 | on a logarithmic scale, because the order of magnitude matters more than the exact value |
| `hidden` | 8 to 128 | any whole number |
| `batch_size` | 16, 32, 64 or 128 | one of the listed values |

Each trial runs `EPOCHS_PER_TRIAL` epochs. The search minimises the validation `mse` at the last epoch and stops after `--trials` trials.

### 4. Try the search on this machine

```bash
python hpo.py --base-task-id <task-id> --local --trials 4
```

`--local` runs the trials as processes on this machine, so no agent is needed. In the web app you get the task **hyperparameter search**, of type *optimizer*, which holds the search, and four tasks named after the base task, one per trial.

### 5. Run the trials on an agent

Send the trials to a queue served by an agent with a GPU. Start that agent as in Example 4, with `--gpus 0`, and name its queue, the one made for that machine, written exactly as **Agents & Queues → Queues** lists it (the machine name plus a short suffix). Then start the search from any machine:

```bash
python hpo.py --base-task-id <task-id> --queue <queue> --trials 20 --concurrent 2
```

> [!NOTE]
> Agent execution is containerized and takes longer than a local run, at least the first time an agent is used: the base image has to be pulled and the environment installed in it before the first step starts. See [Example 4](../04-run-on-an-agent).

`--concurrent 2` runs two trials at a time. Optuna waits for results before it proposes new values, so more concurrent trials are faster but learn a little less from each result. The agents read the private dataset repository with the credential you assigned to it in Example 6.

### 6. Compare the results

Open the task **hyperparameter search**. It lists the objective of every trial, best first. Open the best and the worst trial and compare their **Configuration** and their `mse` curves: a very high learning rate makes the curve jump, and a very small one may not learn within 30 epochs.

The data has noise with standard deviation 0.5, so no model can get the validation `mse` below about `0.5 * 0.5 = 0.25`. When the best trials approach that floor, more search gains little.

> [!NOTE]
> After the first search, narrow a range in `hpo.py`, for example the upper end of `lr`, and search again. See whether the best trial changes.

## Data

Generated by [Example 6](../06-regression-dataset). It is synthetic and has no license restrictions.

## Next steps

Continue with [Example 9: reports and plots](../09-reports-and-plots).
