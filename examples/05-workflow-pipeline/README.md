# A workflow of three steps

This example turns a script into a workflow. The workflow has three steps that depend on each other: prepare the data, train a model, and evaluate the model. CairnML runs each step as its own task, and shows the whole workflow as one run with its steps as a graph.

The steps are the same as in the earlier examples. What is new is how they are organised: each step is an ordinary function, and one more function describes the order.

## What you will learn

- How to split a script into steps with `PipelineDecorator.component`.
- How the pipeline passes the output of one step to the next.
- How to run the whole workflow on one machine, or let agents run each step.

## Before you start

- [Example 4](../04-regression-dataset) is done. It created the dataset repository `examples/greenhouse-data`, and the first step reads the dataset from it.
- The SDK is connected to your server, and the packages are installed (step 1).

## Step 1: Install the packages

```bash
cd examples/05-workflow-pipeline
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Read the three steps

Open `pipeline.py`. Each step is a function with a decorator:

| Step | What it does | What it returns |
|---|---|---|
| `prepare_data` | reads one version of the dataset with `Dataset.get` | the folder with `train.csv` and `test.csv` |
| `train` | trains a small network for a number of epochs | the path of the saved weights and the validation error |
| `evaluate` | loads the weights and scores them on the test file | the R² score, where 1.0 is a perfect fit |

The function `run_workflow` is the pipeline. It does not train anything itself. It only calls the steps, in order:

```python
data_dir = prepare_data(dataset_folder)
model_path, val_mse = train(data_dir, lr, hidden, epochs)
test_r2 = evaluate(data_dir, model_path)
```

Each call returns a value that the next call uses. CairnML records these values, so you can see them in the web app.

Two rules in the code matter. Each step imports what it needs inside its own function, because CairnML runs each step separately. And each step only uses its arguments, not variables from the others.

## Step 3: Run the workflow on this machine

The dataset is given by its repository and commit. By default the script uses the clone that Example 4 created, at its HEAD commit. To use another version, pass the commit, or a URL of the repository:

```bash
python pipeline.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha>
```

Then run the workflow:

```bash
python pipeline.py --local
```

With `--local`, every step runs as a separate task on this machine, one after the other. The script prints the result at the end:

```
workflow done: validation mse 0.41..., test R2 0.97...
```

Your numbers will differ a little, depending on your machine.

To try different settings:

```bash
python pipeline.py --local --lr 0.003 --hidden 64 --epochs 50
```

## Step 4: Look at the run in the web app

Open the project **examples**. The run **greenhouse workflow** is listed as a pipeline. Open it and look at:

- **The graph:** the three steps, `prepare_data`, `train` and `evaluate`, joined in the order they run.
- **Each step:** click a box to open its task. Each task has its own configuration, its log and its console output.
- **The outputs:** `train` shows the validation error, and `evaluate` shows the R² score.

## Step 5: Let agents run the steps

To have an agent run the steps instead of your machine, remove `--local`, and pass the repository URL and the commit that the agent should read:

```bash
python pipeline.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha>
```

The steps are queued on the queue named in `DEFAULT_QUEUE` at the top of `pipeline.py`, which is `default`. An agent on that queue runs each step in turn, as in [example 10](../10-run-on-an-agent). To run `train` on a GPU, change the constant to `DEFAULT_QUEUE = "gpu"`, and start an agent for that queue:

```bash
cairnml-agent daemon --queue gpu --docker --gpus 0
```

Every step gets the same queue in this example. If you want the training on a GPU and the rest on a CPU queue, set `execution_queue` on the `train` step alone.

**Data for the agents.** An agent cannot read the clone on your machine, so pass the URL of the dataset repository and a commit, as in the command above. The first step reads that commit with `Dataset.get`, the same way on your machine and on the agent. Push the dataset repository first, so the commit is on GitHub.

## What to look for

- The steps run in order. `train` does not start before `prepare_data` has returned.
- Running the same pipeline twice creates two runs. Change one parameter and compare the two `train` tasks.
- The validation error of `train` and the test R² of `evaluate`. They are different measures, so compare them across runs rather than against each other: a run with a lower error should also have a higher R².

## Next steps

Continue with the [reports and plots example](../07-reports-and-plots), which shows what you can record next to the scalars.
