# The life of a task

## Goals

Go through the states of a task and the actions you can take on it, and learn which of them can be undone.

What you will learn:

- How a task moves between **Draft**, **Queued**, **Running**, **Completed** and **Published**.
- How to clone a task and change its settings before it runs.
- Which actions are reversible, and which are not.

## Background

A finished run is not the end of a task. You can copy it to run again with other settings, hide it, move it, or freeze it as final. Knowing what each action does, and whether it can be undone, keeps you from losing results by accident.

| Action | Status before | Status after | Can it be undone? |
|---|---|---|---|
| clone | any task | a new draft | yes, delete the copy |
| enqueue | draft | queued | yes, dequeue |
| dequeue | queued | draft | not needed |
| reset | completed or failed | draft | no, the results are removed |
| archive | any | archived | yes, unarchive |
| move | any | unchanged, in another project | yes, move it back |
| publish | completed | published | no |
| delete | any | removed | no |

Only the actions marked "no" need `--yes` in the script. Each one is also in the menus of the web app. The script does them from the command line so that every step is easy to repeat.

## Prerequisites

- About 10 minutes.
- The [SDK connected to your server](../00-installation-and-setup).
- The web app open next to the terminal: each step changes something you can see there.

## Steps

### 1. Install

From the root of the repository:

```bash
source .venv/bin/activate
cd examples/10-task-lifecycle
pip install -r requirements.txt
```

In every new terminal, go to the repository root and run `source .venv/bin/activate` again.

### 2. Create a base task

```bash
python lifecycle.py base
```

This creates the task **lifecycle base** in the project **examples**, logs a short curve and closes it. Its status is **Completed**, and `lr` and `hidden` are listed under **Configuration**. The script keeps its ID in `state.json`.

### 3. Clone it as a draft

```bash
python lifecycle.py clone --lr 0.1
```

A clone has the same code and settings as the original, except the ones you change, here the learning rate. It is named **lifecycle clone** and its status is **Draft**: it does not run until you queue it, and until then its settings can still be edited, in the web app or with the script.

### 4. Queue the clone

```bash
python lifecycle.py enqueue
```

The status becomes **Queued**. The task waits in the `default` queue. No agent serves that queue, because an agent serves only its own ([Example 4](../04-run-on-an-agent)), so it stays queued, which is what this walk through needs. Take it off the queue again with:

```bash
python lifecycle.py dequeue
```

The status returns to **Draft**.

### 5. Reset it

```bash
python lifecycle.py reset --yes
```

A reset removes the results of the clone, its scalars, logs and artifacts, and returns it to a draft. Use it to run the same task again from scratch. The base task is not touched.

### 6. Archive it

```bash
python lifecycle.py archive
```

The clone disappears from the task list. Archiving hides tasks you no longer need without deleting them: click **Open archive** in the web app to see them. Bring it back with:

```bash
python lifecycle.py unarchive
```

### 7. Move it to another project

```bash
python lifecycle.py move --project "examples scratch"
```

The clone moves to the project **examples scratch**, keeping its results and settings. Moving is for organising work.

### 8. Publish the base task

```bash
python lifecycle.py publish --yes
```

Publishing marks a finished task as final. Its outputs become read-only and other tasks can use its models. Nothing reverses it, so publish only what you want to keep unchanged. The script publishes the base task, so the clone can still be deleted in the next step.

### 9. Delete the clone

```bash
python lifecycle.py delete --yes
```

The clone is deleted with its outputs. The base task and any published task are not touched.

### 10. Check the state

```bash
python lifecycle.py status
```

This prints the status of the base task and of the clone. After step 9 the clone is listed as not created.

## Next steps

Continue with [Example 11: import a run](../11-import-external-run).
