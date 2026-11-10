# Run on an agent

## Goals

Run the code of your **private** repository on an **agent**, started from the command line and again from the web app by cloning the task and enqueuing it.

What you will learn:

- How an agent is started, and how it takes work from a **queue**.
- How one script runs either on your machine or on an agent, with `--queue`.
- How to **clone** a task and **enqueue** it in the web app, with no command line.
- What happens when the credential of the repository is missing.

## Background

The agent clones your private repository with the GitHub App credential from [Example 3](../03-private-code-and-credentials), runs `train.py` from the commit the run recorded, and sends the results back to your server.

## Prerequisites

- Time: about 10 minutes, plus the training time.
- [Example 3](../03-private-code-and-credentials) is done: the private repository `cairnml-private-demo` exists, is pushed, and shows **Read with …** on the **Datasets → Repositories** page.
- The [SDK is connected to your server](../00-installation-and-setup) on your own machine.
- A machine with Docker for the agent. It can be your own.

> Note: The agent needs **no Git credentials of its own**. It gets a short-lived read token for the repository from the server, for each job, through the credential you assigned.

## Steps

### 1. Start an agent

On the machine that will run the jobs:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install cairnml-agent
cairnml-agent init http://<server-ip>
cairnml-agent daemon --queue default --docker
```

`init` opens the sign-in page. Sign in with your own account. `daemon --queue default` takes jobs from the shared queue `default`, which is public, and must keep running. Enrolling also made a private queue for this machine, named after it; `daemon` without `--queue` serves that one instead. Add `--gpus 0` to use the first GPU.

**Check:** the machine appears under **Agents & Queues** in the web app.

### 2. Start a run from the command line

On your own machine, in the folder of the private repository, with the packages of the repository installed (it has its own `requirements.txt`):

```bash
cd ~/cairnml-private-demo
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python train.py --epochs 3 --queue default
```

`--queue default` is the only difference from running it locally. The process queues the run and ends. The agent runs the script again from the start, from the **commit that the run recorded**, so the commit must be pushed. If you changed the code, commit and push it first.

The command prints two lines and returns at once:

```
Switching to remote execution, output log page http://<server-ip>/cairnml/...
CairnML Terminating local execution process - continuing execution remotely
```

### 3. Watch the run

In the web app open **Agents & Queues**. The job is listed on the `default` queue until the agent takes it, then it shows on the agent's machine. In the project **examples**, the task **CIFAR-10 classification** goes from **Queued** to **Running** to **Completed**.

On the task:

- **Execution** shows the repository `cairnml-private-demo` and the commit it ran from.
- **Console** starts with the clone of the private repository, then the training output.
- **Scalars** show the loss and accuracy for each epoch.
- **Artifacts** hold the trained model.

### 4. Run it again from the web app

A task in the web app can be copied and started again with other settings, without touching your machine.

1. Open the task from step 3 and click **Clone** (or right-click the task in the list, then **Clone**).
2. In the **Clone Task** dialog, choose the project **examples** and keep or change the name. Click **Clone**. The copy has the status **Draft**.
3. Open the copy. Under **Configuration**, change `epochs` to `5`, for example.
4. Click **Enqueue** (or right-click the task in the list, then **Enqueue**). In the **Enqueue Task** dialog choose the queue `default` and confirm.

The copy goes from **Draft** to **Queued** to **Running** to **Completed**, like the first run. It reads the same repository and the same commit, with your new settings.

> Note: If a repository of the task has no credential, the web app does not enqueue it quietly. It opens **Credentials not assigned**, where you can **Assign credentials** at once.

### 5. See what a missing credential does (optional)

1. In **Datasets → Repositories**, open the row of `cairnml-private-demo` and use the lock button to set it to **Not assigned**.
2. Clone the task again and enqueue it. The web app stops you with **Credentials not assigned**, because the repository is private and no credential reaches it.
3. Click **Assign credentials**, choose your credential and click **Set credential**. Enqueue again: it now runs.

## Troubleshooting

- **The task stays Queued:** no agent listens on the `default` queue. Check that `cairnml-agent daemon --queue default --docker` is still running.
- **The task fails at the start with a repository error:** the credential is missing, or the GitHub App is no longer installed on the repository. Look at the badge on **Datasets → Repositories** and the message of the failed task.
- **The agent cannot find the commit:** the commit was not pushed. Run `git push` in the repository, then run again.
- **`train.py: error: unrecognized arguments: --queue`:** you are running the `train.py` of the public examples repository from an older checkout. Make the folder again with Example 3.

## Next steps

Continue with [Example 5: CIFAR-10 through the dataset registry](../05-cifar-10-managed-dataset), or go to the [task lifecycle](../10-task-lifecycle) to see what else a task can do.
