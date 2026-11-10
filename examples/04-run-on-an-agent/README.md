# Run on an agent

## Goals

Run the code of your private repository on an agent, first from the command line and then from the web app.

What you will learn:

- How an agent takes work from a queue.
- How the same script runs either on your machine or on an agent.
- How to clone a task and enqueue it in the web app, without the command line.

## Background

Training often belongs on a machine other than your laptop, one with a GPU or that stays on. An **agent** is such a machine. You send it work through a **queue**, and it reports everything back to your server, so a run on an agent looks like a local one.

```
your machine                      server                           agent
python train.py --queue default   keeps the job in the queue  <--   takes the job
records repository + commit  ---> and the recorded commit          clones the repository, runs the
                                                                   script, reports back to the server
```

The agent runs the **commit the run recorded**, not what is on your disk, so the code must be pushed. It clones the private repository with the credential from [Example 3](../03-private-code-and-credentials). The agent holds no Git credentials of its own: for each job the server gives it a short-lived read token for that repository.

## Prerequisites

- About 10 minutes, plus the training time.
- [Example 3](../03-private-code-and-credentials) done: the repository `cairnml-private-demo` is pushed and shows **Read with …** on **Datasets → Repositories**.
- The [SDK connected to your server](../00-installation-and-setup).
- A machine with Docker for the agent. It can be your own.

## Steps

### 1. Start an agent

On the machine that will run the jobs, in the environment from Example 0. If that is another machine, create the environment there as in Example 0:

```bash
source .venv/bin/activate
pip install cairnml-agent
cairnml-agent init http://<server-ip>
cairnml-agent daemon --queue default --docker
```

In every new terminal on that machine, go to the repository root and run `source .venv/bin/activate` again before using `cairnml-agent`.

`init` opens the sign-in page. Sign in with your own account. `daemon` takes jobs from the shared `default` queue and must keep running. `--docker` runs every job in its own container. Add `--gpus 0` to use the first GPU.

Enrolling also made a queue for this machine, named after it. `daemon` without `--queue` serves that one. The agent's own key is in `~/.cairnml/agent/`, apart from the SDK's.

Check: the machine appears under **Agents & Queues** in the web app.

### 2. Start a run from the command line

From the root of the examples repository, on your own machine:

```bash
source .venv/bin/activate
cd ../cairnml-private-demo
pip install -r requirements.txt
python train.py --epochs 3 --queue default
```

In a new terminal, go to the root of the examples repository and run `source .venv/bin/activate` first. `--queue default` is the only difference from a local run. The command queues the run and ends:

```
Switching to remote execution, output log page http://<server-ip>/cairnml/...
CairnML Terminating local execution process - continuing execution remotely
```

If you change the code, commit and push before you run again.

### 3. Watch the run

Under **Agents & Queues** the job waits on the `default` queue until the agent takes it, then shows on the agent's machine. In the project **examples** the task **CIFAR-10 classification** goes from **Queued** to **Running** to **Completed**. On the task:

- **Execution** shows the repository `cairnml-private-demo` and the commit it ran from.
- **Console** starts with the clone of the private repository, then the training output.
- **Scalars** and **Artifacts** hold the curves and the trained model, as in Example 2.

### 4. Run it again from the web app

A task can be copied and started with other settings without touching your machine.

1. Open the task and click **Clone**. In the **Clone Task** dialog keep the project **examples** and click **Clone**. The copy has the status **Draft**.
2. Open the copy and change `epochs` to `5` under **Configuration**.
3. Click **Enqueue**, choose the queue `default` and confirm.

The copy runs like the first one, from the same repository and commit, with your new settings. Because the commit is kept, a clone is also how you rerun exactly the same code later.

### 5. See what a missing credential does (optional)

1. In **Datasets → Repositories**, open the row of `cairnml-private-demo` and set its credential to **Not assigned**.
2. Clone the task and enqueue it. The web app stops you with **Credentials not assigned**: the repository is private and no credential reaches it.
3. Click **Assign credentials**, choose your credential and click **Set credential**. Enqueue again, and it runs.

## Troubleshooting

- **The task stays Queued:** no agent serves the `default` queue. Check that `daemon` is still running.
- **The task fails at the start with a repository error:** the credential is missing, or the App is no longer installed on the repository. Check the badge on **Datasets → Repositories** and the message of the failed task.
- **The agent cannot find the commit:** it was not pushed. Run `git push`, then run again.
- **`unrecognized arguments: --queue`:** the folder was made from an older `train.py`. Make it again with Example 3.

## Next steps

Continue with [Example 5: CIFAR-10 through the dataset registry](../05-cifar-10-managed-dataset).
