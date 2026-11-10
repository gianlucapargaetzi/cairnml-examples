# A workflow of three steps

## Goals

Split a script into three dependent steps, prepare the data, train and evaluate, and run them as one workflow.

What you will learn:

- How to turn functions into pipeline steps with `PipelineDecorator.component`.
- How the output of one step becomes the input of the next.
- Why a step can run on another machine than the rest.

## Background

In the earlier examples one script did everything. A **pipeline** splits that work into steps. CairnML runs each step as a task of its own, and shows the whole workflow as one run with its steps as a graph.

Why split it:

- **Each step is visible on its own,** with its configuration, console and results, so you can see where a run went wrong.
- **Each step can run somewhere else.** Preparing data needs no GPU, training does. A step can be sent to a queue of its own.
- **Steps are reusable and comparable.** Run the pipeline twice with another learning rate and compare the two `train` tasks.

Each step is an ordinary function with a decorator, and one more function describes the order:

```python
data_dir = prepare_data(dataset_repo, dataset_commit)
model_path, val_mse = train(data_dir, lr, hidden, epochs)
test_r2 = evaluate(data_dir, model_path)
```

The pipeline function trains nothing itself. Each return value is recorded and handed to the next step. Because every step runs separately, possibly on another machine, a step must import what it needs inside its own function and may only use its arguments, not variables of the others.

## Prerequisites

- About 10 minutes.
- [Example 6](../06-regression-dataset) done. Its repository URL and commit are passed as `--repo` and `--commit`; the first step reads that version with `Dataset.get`.
- The [SDK connected to your server](../00-installation-and-setup).

## Steps

### 1. Install

```bash
cd examples/07-workflow-pipeline
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 2. Read the steps

Open `pipeline.py`:

| Step | What it does | What it returns |
|---|---|---|
| `prepare_data` | reads one version of the dataset with `Dataset.get` | the folder with `train.csv` and `test.csv` |
| `train` | trains a small network | the path of the saved weights and the validation error |
| `evaluate` | scores the weights on the test file | the R² score, where 1.0 is a perfect fit |

### 3. Run the workflow on this machine

```bash
python pipeline.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha> --local
```

With `--local` every step runs as a separate task on this machine, one after the other. The script ends with a line like `workflow done: validation mse 0.41..., test R2 0.97...`. Your numbers will differ a little. To read another version of the data, pass its commit. To try other settings add, for example, `--lr 0.003 --hidden 64 --epochs 50`.

### 4. Look at the run

In the project **examples**, open the run **greenhouse workflow**:

- **The graph** shows `prepare_data`, `train` and `evaluate` in the order they run.
- **Each box** opens the task of that step, with its own configuration and console output.
- `train` shows the validation error and `evaluate` the R² score. They measure different things, so compare each across runs: a lower error should come with a higher R².

### 5. Let an agent run the steps

Remove `--local` to queue the steps for an agent, as in [Example 4](../04-run-on-an-agent):

```bash
python pipeline.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha>
```

The steps go to the queue named by `DEFAULT_QUEUE` at the top of `pipeline.py`, `default`. The agent reads the private dataset repository the same way your machine does, with the credential and the App installed in Example 6, and the server gives each job read access to it.

To train on a GPU and prepare the data on a CPU, set `execution_queue` on the `train` step alone, to the queue of the agent that has the GPU. Each agent has a queue named after its machine, listed under **Agents & Queues**.

## Next steps

Continue with [Example 8: hyperparameter optimisation](../08-hyperparameter-optimisation).
