# Installation and setup

## Goals

Get from a running server to a signed-in account and a machine enrolled with the SDK, with the vocabulary every other example uses.

What you will learn:

- How you get an account and sign in.
- What the pages of the web app are for.
- What **task**, **experiment**, **agent** and **job** mean.
- What the **credentials** in the web app are for.
- How to install the SDK and enrol your machine.

## Background

CairnML is a self-hosted platform for machine learning work. It records every run of your code with its settings, curves and results, so that runs can be compared and repeated. It can also run your code on other machines, and it versions the data your runs use.

It has four parts:

- **The server** stores everything and serves the web app. It runs once, for everyone.
- **The web app** is where you look at your runs, models, datasets and machines.
- **The SDK** (`cairnml`) is a Python package you install next to your code. A few lines in a script record the run on the server.
- **The agent** (`cairnml-agent`) runs on a machine that should execute jobs. It takes work from a queue.

Code and datasets live in GitHub repositories. CairnML reads them when a job needs them.

## Prerequisites

- About 15 minutes.
- The address of your server, called `<server-ip>` below. Add a port only if the server does not use port 80, for example `<server-ip>:8081`.
- An admin of the server who can create your account. If you run the server yourself, that is you.

## Steps

### 1. Get an account

There is no self-registration: an admin creates every account, in the sign-in service (Keycloak) of the server. If you are not the admin, send yours your name and email address, and ask for a username and a first password.

If you are the admin:

1. Open `http://<server-ip>/cairnml/idp/admin` and sign in with `KC_ADMIN` and `KC_ADMIN_PASSWORD` from `deploy/.env` of the server (`cairnadmin` by default).
2. Choose the `cairnml` realm in the selector at the top left.
3. Open **Users**, then **Add user**. Enter a username, email and name, and turn on **Email verified**.
4. On the new user's **Credentials** tab, click **Set password**, enter a password and turn **Temporary** off.
5. Only for another admin: give the user the realm role `cairnml-admin` on the **Role mapping** tab.

To sign in to the web app as the admin yourself, use `KC_ADMIN` with `CAIRNML_ADMIN_PASSWORD`, also from `deploy/.env`. More in the [server README](https://github.com/gianlucapargaetzi/cairnml-server#users-and-admins).

### 2. Sign in to the web app

Open `http://<server-ip>/cairnml/` and sign in. Your CairnML account is created at your first sign-in.

Check: the **Projects** page opens. It is empty on a new server.

> [!TIP]
> Keep the web app open in a second window next to your terminal. Every example changes something there that you can look at.

### 3. Take the tour of the web app

The side bar on the left leads to the main areas:

| Entry | What it is for |
|---|---|
| **Projects** | Your work, in folders called projects. A project holds tasks, models and reports. Most of what you do happens here |
| **Pipelines** | Workflows made of several steps, each step its own task |
| **Datasets** | Versioned data, and the code repositories CairnML reads |
| **Agents & Queues** | The machines that run your jobs, and the queues they take jobs from |

At the bottom are **Search all**, **Help** and the **Account** menu, which leads to **Settings**.

**Settings** has these pages:

| Page | What it is for |
|---|---|
| **Profile** | Your name |
| **User preferences** | How the web app looks and behaves for you |
| **Devices** | The machines enrolled for your account, your laptop and your agents. You can revoke one |
| **Access** | The credentials that let CairnML read private code and data (step 5) |

### 4. Learn the words

| Word | Meaning |
|---|---|
| **Task** | A piece of code that can be run, a "code snippet": a training script, a pipeline step, an evaluation |
| **Experiment** | One execution of a specific task, with its settings, curves and results. Run a task twice and you have two experiments |
| **Agent** | A remote worker: a machine that runs `cairnml-agent` and takes work from a queue |
| **Job** | A snippet scheduled to run on an agent: an experiment, a pipeline step or anything else that was queued |

How they fit together: you write a task and run it, which makes an experiment. If you queue it instead of running it here, it becomes a job that waits in a **queue** until an agent takes it and runs it. The result is recorded as an experiment in the web app, like a local run.

Two more words come up often. A **project** is a folder for related tasks, models and reports. A **queue** is a waiting line for jobs: every agent has its own, made when the agent is enrolled, and an agent serves only that one.

### 5. Know what the credentials are for

Open **Settings → Access**. It is empty now, and that is fine.

A **credential** is a GitHub App that CairnML may use to read a repository that is not public. It is needed when an agent has to clone your private code to run a job, and when the server has to read a private dataset repository.

CairnML never uses your own GitHub password or token. You create the App once on GitHub, install it only on the repositories it may read, and add its key here. The key is checked with GitHub, stored encrypted, and never shown again.

You do not need one yet: the first two examples run on your machine and read nothing private. [Example 3](../03-private-code-and-credentials) creates one, [Example 4](../04-run-on-an-agent) uses it for code on an agent, and [Example 6](../06-regression-dataset) uses it for a private dataset.

### 6. Install the SDK

Get these examples and create one Python environment at the top of the repository, on the machine where you write and run your code. Every later example uses this same environment:

```bash
git clone https://github.com/gianlucapargaetzi/cairnml-examples.git
cd cairnml-examples
python3 -m venv .venv
source .venv/bin/activate
pip install cairnml
```

The environment keeps the packages of the examples apart from the rest of your machine, and each example adds its own requirements to it. In every new terminal, go to the root of the repository and run `source .venv/bin/activate` before you use `cairnml` or run an example. All later examples start from that folder.

### 7. Enrol your machine

```bash
cairnml init http://<server-ip>
```

Your browser opens the sign-in page. Sign in with your user. The terminal prints `enrolled as ...` when the machine is connected.

The machine gets a key of its own, tied to your user. Nothing is shared between machines, and no secret is typed into a script. The key is stored in `~/.cairnml/device.key`, the folder where CairnML keeps what is specific to this machine. Keep it private and do not copy it to another machine: enrol each machine on its own.

On a machine without a browser, such as a remote shell or a container, the command shows a short code and an address instead. Open the address on any device, sign in, and enter the code. Add `--device` to use this sign-in on any machine.

Check: **Settings → Devices** lists your machine with the kind **Client**. You can revoke it there at any time.

## Troubleshooting

- **The sign-in is refused:** the username or password is wrong, or the admin has disabled the account.
- **`cairnml init` cannot reach the server:** check the address and port. The web app must open at `http://<server-ip>/cairnml/` from this machine.
- **No browser opens:** copy the address the command prints, or use `--device`.
- **The machine is not listed under Devices:** run `cairnml init http://<server-ip>` again.

## Next steps

Continue with [Example 1: hello world](../01-hello-world).
