# The life of a task

## Goals

Go through everything a task can do after it has run: clone, queue, reset, archive, move, publish and delete.

What you will learn:

- The states a task goes through: draft, queued, running, completed, published.
- How to copy a task and change its settings before it runs.
- What archiving, moving and publishing change, and which of them can be undone.

## Background

A task in CairnML is more than a finished run. It can be copied, queued, archived, moved to another project, published and deleted. This example walks through each of these actions in order, with one command per step, so you can see what each one changes in the web app.

Every action in this example is also in the web app's menus. The script does the same things from the command line, which makes each step easy to repeat.

## Before you start

- Time: about 10 minutes.
- The SDK is connected to your server, and the package is installed (step 1).
- Keep an eye on the web app while you go through the steps. Each step tells you what to look for.

## Steps

### 1. Install the package

```bash
cd examples/10-task-lifecycle
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a base task

```bash
python lifecycle.py base
```

The script creates a task named **lifecycle base** in the project **examples**, logs a short curve, and closes the task. The task's status is **Completed**. It is the starting point for the rest of the steps, and the script saves its ID in `state.json`.

Look at it in the web app. Its status is **Completed**, and its settings are `lr` and `hidden` under **Configuration**.

### 3. Clone it as a draft

```bash
python lifecycle.py clone --lr 0.1
```

A clone is a copy of the base task: the same code and the same settings, except the ones you change. The script sets the learning rate of the copy to `0.1`. The copy is named **lifecycle clone**, and its status is **Draft**.

A draft can still be changed. Its settings can be edited in the web app or with the script, and it does not run until you queue it.

### 4. Queue the clone

```bash
python lifecycle.py enqueue
```

The status changes to **Queued**. The task waits in the `default` queue until an agent takes it. To run it, start an agent for that queue, as in [example 4](../04-run-on-an-agent). Without an agent, the task stays queued.

Take it off the queue again if you change your mind:

```bash
python lifecycle.py dequeue
```

The status returns to **Draft**. Queue it once more before step 5 if you want it to run.

### 5. Reset it

A reset removes the results of a task (its scalars, its logs and its artifacts) and returns it to a draft. Use it when a run has failed or you want to run the same task again from scratch.

```bash
python lifecycle.py reset --yes
```

The script refuses to run without `--yes`. The reset removes the results of the clone only, not the base task.

### 6. Archive it

```bash
python lifecycle.py archive
```

The clone disappears from the task list. Archiving is a way to hide tasks you no longer need, without deleting them. Click **Open archive** in the web app to see archived tasks.

```bash
python lifecycle.py unarchive
```

The task is back in the list, with its status unchanged.

### 7. Move it to another project

```bash
python lifecycle.py move --project "examples scratch"
```

The clone moves to the project **examples scratch**. Moving is for organising work: the task keeps its results and its settings.

### 8. Publish the base task

```bash
python lifecycle.py publish --yes
```

Publishing marks a finished task as final. Its outputs become read-only, so nothing can change them, and other tasks can use its models. The status changes to **Published**.

Treat publishing as final: this example has no step that reverses it, so the script asks for `--yes`. Only publish a task you are sure you want to keep unchanged. This example publishes the base task, not the clone, so the clone can still be deleted in the next step.

### 9. Delete the clone

```bash
python lifecycle.py delete --yes
```

The clone is deleted, together with its outputs. The base task is not touched, and neither is any published task.

### 10. Check the state

```bash
python lifecycle.py status
```

Prints the status of the base task and of the clone. After step 9, the clone is listed as not created.

## What to look for

You end with a base task, a clone, and a feel for every action a task allows.

| Action | Status before | Status after | Can it be undone? |
|---|---|---|---|
| clone | (a completed task) | a new draft | yes, delete the copy |
| enqueue | draft | queued | yes, dequeue |
| dequeue | queued | draft | not needed |
| reset | completed or failed | draft | no, the results are removed |
| archive | any | archived | yes, unarchive |
| move | any | any, in another project | yes, move it back |
| publish | completed | published | no |
| delete | any | removed | no |

Only the steps marked "no" need `--yes`. The others are reversible, so the script runs them directly.

## Next steps

Continue with [Example 11: import a run](../11-import-external-run), which brings a run from a project that does not use CairnML into the web app.
