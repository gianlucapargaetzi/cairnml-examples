# Private code and credentials

## Goals

Put your training code in a **private** GitHub repository and give CairnML a key that can read it, so that an agent can run the code in [Example 4](../04-run-on-an-agent).

What you will learn:

- Why CairnML reads private code through a **GitHub App** and not through a password or a token of yours.
- How to create the App, install it on one repository only, and add its key to CairnML.
- How a repository gets its credential: the **Repositories** page, and the badge that tells you how it is read.

## Background

You will make a private repository from the training code of [Example 2](../02-cifar10-classification), create a **GitHub App** that may read only that repository, add the App to CairnML as a **credential**, and assign it to the repository. Nothing runs in this example. It ends when CairnML shows the repository as readable.

## Before you start

- Time: about 15 minutes.
- The [SDK connected to your server](../00-installation-and-setup) and **Example 1** run once, so the project **examples** exists.
- An account in the web app. Any user can add a credential of their own; only an admin can add one for the whole company.
- The GitHub command line `gh` is **optional**. Every step that can use it also has a way to do it in the browser.

## Steps

### 1. Make the repository folder

```bash
cd examples/03-private-code-and-credentials
python make_private_repo.py ~/cairnml-private-demo
```

The script copies `train.py` and `requirements.txt` from Example 2 into a new folder, outside this repository, and makes the first commit. It needs git and nothing else. The new folder is the repository you publish next.

> Note: The copy of `train.py` can queue itself for an agent with `--queue`. That is what Example 4 uses.

### 2. Publish it as a private repository

Choose one way. Both end with a **private** repository named `cairnml-private-demo` under your account, holding the commit from step 1.

**Option A: with the GitHub command line.** Log in once with `gh auth login`, then:

```bash
cd ~/cairnml-private-demo
gh repo create cairnml-private-demo --private --source . --push
```

**Option B: in the browser.**

1. Open [github.com/new](https://github.com/new).
2. Enter the name `cairnml-private-demo` and choose **Private**.
3. Leave **Add a README**, **.gitignore** and **license** switched off: the folder already has its files.
4. Click **Create repository**. Then, in the folder, use the address GitHub shows:

```bash
cd ~/cairnml-private-demo
git remote add origin https://github.com/<your-user>/cairnml-private-demo.git
git push -u origin main
```

Git asks you to sign in. Use your browser login through the credential helper of your system, or use the SSH address `git@github.com:<your-user>/cairnml-private-demo.git` if you have an SSH key on GitHub.

**Check:** open the repository in a private browser window where you are not signed in. GitHub shows *404 Not Found*. That is what a private repository looks like to everyone else, and to CairnML until you finish this example.

### 3. Create the GitHub App

CairnML never uses your own login. It reads a repository through a **GitHub App**: a small identity that you create once, give read access, and install on the repositories it may read. Creating one is done on GitHub, in the browser. Neither `gh` nor the SDK can do it.

1. On GitHub open **Settings → Developer settings → GitHub Apps → New GitHub App**. For an organisation, use the same page under the organisation's settings.
2. Fill in:
   - **GitHub App name:** for example `cairnml-<your-name>`. The name must be unique on GitHub.
   - **Homepage URL:** any address, for example the address of your repository.
   - **Webhook:** switch **Active** off. CairnML needs no webhook.
   - **Repository permissions → Contents:** **Read-only**. Leave every other permission at **No access**. CairnML only reads.
   - **Where can this GitHub App be installed?** **Only on this account**.
3. Click **Create GitHub App**. Note the **App ID** at the top of the page: a number.
4. Under **Private keys**, click **Generate a private key**. Your browser saves a `.pem` file. It is the secret half of the App: keep it, and do not commit it anywhere.

### 4. Install the App on the repository, and only on it

1. On the App's page, open **Install App** and choose your account.
2. Choose **Only select repositories**, pick `cairnml-private-demo`, and click **Install**.

>  Least privilege: this App can read one repository and nothing else. A repository that is not selected here stays unreadable, even for CairnML.

### 5. Add the App to CairnML as a credential

1. In the web app open **Settings → Access** and click **Add credential**.
2. Enter a **Name** (for example `my github app`) and the **App ID** from step 3. Leave **API address** empty for github.com.
3. Click **Choose key file** and select the `.pem` file.
4. Click **Add credential**.

CairnML checks the key with GitHub before it saves anything, then keeps it encrypted on the server. The key is never shown again.

**Check:** the credential is listed with a working status. The same list is available in the terminal:

```bash
cairnml credential list
```

An admin also sees **Valid for**. Choose **Only me** here: the credential is then yours, and nobody else can use it.

### 6. Add the repository and assign the credential

1. In the web app open **Datasets**, then the **Repositories** tab, and click **Add repository**.
2. Enter `https://github.com/<your-user>/cairnml-private-demo` and choose the project **examples**. Click **Add repository**.
3. The repository is listed with the badge **No credential assigned**. Open its row with the arrow on the left, and click the lock button **Assign credentials**.
4. Choose your credential and click **Set credential**.

CairnML asks GitHub for a read token for this repository with your App, so the step only succeeds when the App is installed on it.

**Check:** the badge now says **Read with my github app** (the name you gave the credential).

The same thing is available in the project: **project settings → Repositories**, for the project **examples**.

## What to look for

You end with a private repository, a GitHub App, and a credential that reads the repository.

| Where | What you see | What it means |
|---|---|---|
| **Settings → Access** | one credential, working status | CairnML can use the App's key |
| **Datasets → Repositories** | `cairnml-private-demo`, badge **Read with …** | the repository is read with that credential |
| Private browser window | 404 on GitHub | the repository really is private |

## Troubleshooting

- **`the GitHub App … is not installed on …`** when you click **Set credential**: step 4 is missing, or the App was installed on another account. Install it on the account that owns the repository and select the repository.
- **`You have no credentials to choose from`** in the dialog: step 5 is missing. Add the credential in **Settings → Access**.
- **The key is refused** in step 5: the App ID and the `.pem` file belong to different Apps, or the key is for a GitHub Enterprise server (then fill in **API address**).
- **The project `examples` is not in the list** in step 6: run [Example 1](../01-hello-world) first, or choose **No project**.
- **There is no lock button:** only the project's owner, the user who first used the repository there, or an admin can assign a credential.

## Next steps

Continue with [Example 4: run on an agent](../04-run-on-an-agent). It runs the code from your private repository on an agent, with the credential you just made.
