<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/cairnml-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/cairnml-logo.svg">
    <img src="assets/cairnml-logo.svg" alt="CairnML" width="480">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/gianlucapargaetzi/cairnml-examples/stargazers"><img src="https://img.shields.io/github/stars/gianlucapargaetzi/cairnml-examples?style=flat-square&logo=github" alt="GitHub stars"></a>
</p>

# CairnML Examples

Guided examples of what the CairnML platform can do. Each example runs on your own server and records its run there. The examples build on each other: start with the hello world, then the CIFAR-10 classification, then the two COCO Fashion examples, which train the same detector on the same images in two different ways.

## Features

- Five runnable examples, from a single tracked run to a full training run, and a run sent to an agent.
- Runs appear in the web app, with their parameters, metrics, loss curves and artifacts.
- The fourth example reads its data through the dataset registry, so the run records which dataset and revision it used.
- Examples 3 and 4 train on the same images, so their runs can be compared side by side.

## Prerequisites

- Python 3.9 or newer
- The [SDK](https://github.com/gianlucapargaetzi/cairnml) connected to a running [CairnML server](https://github.com/gianlucapargaetzi/cairnml-server):

```bash
pip install cairnml
cairnml init http://<server-ip>
```

`<server-ip>` is the address of the server, with a port only if the server does not use port 80. The command works out the rest.

## Examples

| Example | What it shows |
|---|---|
| [Hello world](examples/01-hello-world) | One run with parameters, a metric curve and an artifact |
| [CIFAR-10 classification](examples/02-cifar10-classification) | Multiclass classification of small photographs, with a loss curve and test accuracy |
| [COCO Fashion detection](examples/03-coco-fashion-detection) | Training a detector on downloaded data, without a registry |
| [COCO Fashion through the dataset registry](examples/04-coco-fashion-managed-dataset) | The same training, reading the data through the dataset registry |
| [Run on an agent](examples/05-run-on-an-agent) | The hello world run, executed on a machine running `cairnml-agent` through the `default` queue |

Each example has its own README with the installation steps, the command to run and what to look for in the web app.

## Walk-through: from a local run to an agent

This walk-through follows the core loop: track a run from your machine, send it to an agent, watch it, and inspect the results. Do the steps in order. Each step ends with what you should see. You need the address of your server, the SDK installed, and an admin account on the server for step 3.

### 1. Connect this machine

```bash
pip install cairnml
cairnml init http://<server-ip>
```

Your browser opens the sign-in page. The terminal prints `enrolled as ...` when this machine is connected.

### 2. Track a run from this machine

```bash
cd examples/01-hello-world
pip install -r requirements.txt
python hello_world.py
```

The script prints `done: the run is in the web app, project 'examples', task 'hello world'`. The run executed on this machine and was recorded on the server. In the web app, open project **examples**, task **hello world**: the parameters, a `loss` curve and `hello.txt` under artifacts are there.

### 3. Start an agent on the machine that will run the jobs

On the machine that will run the jobs, which needs Docker:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install cairnml-agent
cairnml-agent init http://<server-ip>
cairnml-agent daemon --queue default --docker
```

`init` opens the sign-in page; sign in as an admin, because only admins can enrol an agent. `daemon` listens on the `default` queue and must keep running. The machine appears under **Workers & Queues** in the web app. Add `--gpus 0` to the `daemon` command to let the agent use the first GPU.

### 4. Send the run to the agent

The agent clones the repository from GitHub, so commit and push your changes first. Then:

```bash
cd examples/05-run-on-an-agent
python run_on_agent.py
```

The command returns at once. It prints two warnings: `Switching to remote execution, output log page ...` and `CairnML Terminating local execution process - continuing execution remotely`. The local process has stopped; the agent runs the script.

### 5. Watch the run

Open **Workers & Queues**: the job is listed on the `default` queue until the agent takes it, then the agent's machine shows it as running. In project **examples**, task **run on an agent** moves from **Queued** to **Running** to **Completed**.

### 6. Inspect the results

Open task **run on an agent**:

- **Scalars:** the `loss` curve, one point per step.
- **Artifacts:** `hello.txt`.
- **Console:** the script's output as the agent ran it, ending with the `done:` line.
- **Configuration:** the `greeting` and `steps` parameters.

If the task stays **Queued**, no agent is listening on the `default` queue. Check that the `daemon` command from step 3 is running on the agent's machine. The [example 5 README](examples/05-run-on-an-agent) lists the other prerequisites.

## Compare the runs

Examples 3 and 4 use the same model, settings and images. After both have run, open the **COCO Fashion** project in the web app and compare the two tasks. Their validation mAP curves should be close, and the configuration of the fourth run shows the dataset, its revision and the registry commit.

## Having problems

1. Check the [open issues](https://github.com/gianlucapargaetzi/cairnml-examples/issues).
2. If your problem is not listed, [open a new issue](https://github.com/gianlucapargaetzi/cairnml-examples/issues/new) with the example you ran, the command, and the full error message.
