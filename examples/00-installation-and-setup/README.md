# Installation and setup

## Goals

Get from a running server to a signed-in account and a machine enrolled with the SDK, with the vocabulary every other example uses.

What you will learn:

- How an account is made and how you sign in for the first time.
- What the pages of the web app are for.
- The words used everywhere in the examples: **task**, **experiment**, **agent**, **job**.
- What the **credentials** in the web app are for, and where the examples use them.
- How to install the SDK and enrol your machine with your own user.

## Background

Nothing is recorded in this example. It prepares your account, your machine and your head.

## Before you start

- Time: about 15 minutes.
- The address of your server, called `<server-ip>` below. Add a port only if the server does not use port 80, for example `<server-ip>:8081`.
- Someone who can create accounts: an **admin** of the server. If you run the server yourself, that is you.

## Steps

### 1. Get an account

CairnML has no self-registration. An admin creates every account, in the sign-in service (Keycloak) of the server.

**If you are not the admin:** ask your admin for an account. Send your name and your email address, and ask for a username and a first password.

**If you are the admin**, create the account like this:

1. Open `http://<server-ip>/cairnml/idp/admin` and sign in as the admin user of the server. Its name and password are `KC_ADMIN` and `KC_ADMIN_PASSWORD` in `deploy/.env` of the server (`cairnadmin` by default).
2. Choose the `cairnml` realm in the selector at the top left.
3. Open **Users**, then **Add user**. Enter a username, email and name, and turn on **Email verified**. Click **Create**.
4. On the new user's **Credentials** tab, click **Set password**, enter a password and turn **Temporary** off.
5. To make the user an admin too, give them the realm role `cairnml-admin` on the **Role mapping** tab. Most users do not need it.

The details are in the [server README](https://github.com/gianlucapargaetzi/cairnml-server#users-and-admins).

> Note: The admin of a fresh server signs in to the web app with the user `KC_ADMIN` and the password `CAIRNML_ADMIN_PASSWORD`, both from `deploy/.env`.

### 2. Sign in to the web app

1. Open `http://<server-ip>/cairnml/` in your browser.
2. Sign in with your username and password.

Your CairnML account is created at your first sign-in. Nothing else is needed.

**Check:** you see the **Projects** page. It is empty on a new server.

### 3. Take the tour of the web app

The **side bar** on the left leads to the main areas:

| Entry | What it is for |
|---|---|
| **Projects** | Your work, in folders called projects. A project holds tasks, models and reports. Most of what you do happens here |
| **Pipelines** | Workflows made of several steps, each step its own task (Example 7) |
| **Datasets** | Versioned data, and the code repositories CairnML reads (Examples 3 and 6) |
| **Agents & Queues** | The machines that run your jobs, and the queues they take jobs from (Example 4) |

At the bottom of the side bar are **Search all**, **Help** and the **Account** menu. The account menu leads to **Settings**.

Open a project, for example **examples** once Example 1 has run. It has tabs:

| Tab | What it shows |
|---|---|
| **Overview** | A summary of the project |
| **Workloads** | What is running and queued for the project |
| **Tasks** | The tasks as folders |
| **Task list** | The same tasks as a table, to sort, filter and compare |
| **Models** | The models made by tasks |
| **Project settings** | Who may use the project, its queues, datasets, credentials and repositories |

Open **Settings** from the account menu:

| Page | What it is for |
|---|---|
| **Profile** | Your name |
| **User preferences** | How the web app looks and behaves for you |
| **Devices** | The machines enrolled for your account: your laptop and your agents. You can revoke one |
| **Access** | The **credentials** that let CairnML read private code and data (see step 5) |

### 4. Learn the words

Four words are used in every example, and they are easy to mix up.

| Word | Meaning |
|---|---|
| **Task** | A piece of code that can be run, a "code snippet": a training script, a pipeline step, an evaluation |
| **Experiment** | One execution of a specific task: one run of it, with its settings, its curves and its results. Run a task twice and you have two experiments |
| **Agent** | A remote worker: a machine that runs `cairnml-agent` and takes work from a queue |
| **Job** | A snippet scheduled to run on an agent: an experiment, a pipeline step or anything else that was queued, until an agent runs it |

How they fit together: you write a **task** and run it, which makes an **experiment**. If you queue it instead of running it here, it becomes a **job** that waits in a **queue** until an **agent** takes it and runs it. The result is recorded as an experiment in the web app, like a local run.

Three more words come up often:

| Word | Meaning |
|---|---|
| **Project** | A folder for related tasks, models and reports. The examples use the project **examples** |
| **Queue** | A waiting line for jobs. Every agent has its own queue, made when the agent is enrolled; the server also has a shared `default` queue |
| **Dataset** | Data kept in a git repository, versioned, with the commit as its version (Examples 5 and 6) |

### 5. Know what the credentials are for

Open **Settings → Access**. It is empty now, and that is fine.

A **credential** is a **GitHub App** that CairnML may use to read a repository that is not public. CairnML needs one in two situations:

- **Code:** an agent has to clone your **private** code repository to run a job from it.
- **Data:** the server has to read a **private** dataset repository.

CairnML never uses your own GitHub password or token. You create the App once, on GitHub, install it on only the repositories it may read, and add its key here. The key is checked with GitHub, stored encrypted, and never shown again.

You do not need one for the first examples: Examples 1 and 2 run on your machine and read nothing private. Credentials are created and used in **[Example 3](../03-private-code-and-credentials)**, used by an agent in **[Example 4](../04-run-on-an-agent)**, and used for a private dataset in **[Example 6](../06-regression-dataset)**.

### 6. Install the SDK

On the machine where you write and run your code:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install cairnml
```

A virtual environment keeps the packages of the examples apart from the rest of your machine. Activate it again in every new terminal.

### 7. Enrol your machine with your user

```bash
cairnml init http://<server-ip>
```

Your browser opens the sign-in page. Sign in with the user from step 1. The terminal prints `enrolled as ...` when the machine is connected. The command works out the rest of the configuration from the address.

CairnML gives the machine a key of its own, so nothing is shared between machines and nothing secret is typed in a script. The key belongs to your user.

**On a machine without a browser**, such as a remote shell or a container, the command shows a short code and an address instead. Open the address on any device, sign in, and enter the code. Add `--device` to use this sign-in on any machine.

**Check:** in the web app, open **Settings → Devices**. Your machine is listed, with the name of the machine and the kind **Client**. You can revoke it there at any time.

## What to look for

You end with an account, a first sign-in, a tour of the web app, the terminology, and an enrolled machine.

- You can sign in, and the **Projects** page opens.
- **Settings → Devices** lists your machine.
- You can say, in one sentence each, what a task, an experiment, an agent and a job are.

## Troubleshooting

- **The sign-in is refused:** the username or the password is wrong, or the admin has disabled the account. Ask the admin.
- **`cairnml init` cannot reach the server:** check the address, and the port if the server does not use port 80. The web app must open at `http://<server-ip>/cairnml/` from this machine.
- **No browser opens:** copy the address the command prints, or use `--device`.
- **The machine is not listed under Devices:** run `cairnml init http://<server-ip>` again.

## Next steps

Continue with [Example 1: hello world](../01-hello-world), your first run.
