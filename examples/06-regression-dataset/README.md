# 🌱 A regression dataset in its own repository

> 🎯 **Goal:** build a small dataset on your machine, publish it as a **private dataset repository**, and read one exact version of it in training code. The next examples train on it.

The problem is made up but reads like a real one. A small greenhouse uses energy to heat itself. Given the weather and the time of day, the model should predict how many kWh per hour it needs. A script generates the data from a seed, so anyone who runs it gets the same files and nothing is downloaded.

The dataset repository is not a folder of this example. You create it in a temporary folder outside the examples, and that folder is the repository that is published to GitHub.

| | |
|---|---|
| ⏱️ **Time** | about 20 minutes |
| 🧰 **Needs** | Python 3.9 or newer, [git](https://git-scm.com), the SDK connected to your server, and the GitHub App from [Example 3](../03-private-code-and-credentials) |
| 📦 **You end with** | a private dataset repository, its commit, and a task that read it |

## 📚 What you will learn

- How a dataset is a git repository: git holds the metadata, and the files are held in the dataset storage of your server.
- How a **credential** lets the server read the private repository, as in Example 3.
- How a run records the repository, the commit and the content hash of the data it read.

## ✨ Features

- Generates two CSV files from a seed, so the same parameters always give the same data.
- Reads the CSV files through `adapter.py`, a local adapter in the dataset repository. The check runs it on your machine and checks every sample against the CairnML dataset format.
- Sets the dataset up locally first, then connects it to a **private** repository that you create on GitHub.
- Makes the repository visible to the framework through your GitHub App, so the server can read it for jobs and list it.
- Reads one version with `Dataset.get`, and records the repository, the commit and the content hash on the run.

## ✅ Before you start

- Python 3.9 or newer, and [git](https://git-scm.com).
- The [SDK connected to your server](../00-installation-and-setup). `cairnml dataset remote add` registers the repository with the server and sets up its dataset storage, so it needs the connection. The local commands do not.
- The **GitHub App credential** of [Example 3](../03-private-code-and-credentials), working in **Settings → Access**. Step 6 installs it on the new repository.
- The [GitHub command line](https://cli.github.com), `gh`, is **optional**. Where a step uses it, the same step also shows how to do it in the browser.

## 🚀 Steps

### 1. Install the tools

Create a virtual environment and install the requirements:

```bash
cd examples/06-regression-dataset
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Check that the dataset commands are installed:

```bash
cairnml dataset --help
```

You should see the commands `init`, `remote`, `add`, `commit`, `push`, `doctor` and `get`, among others.

### 2. Look at the generator

Open `generate.py`. It draws five input columns and one target, `energy`:

| Column | Meaning | Effect on energy |
|---|---|---|
| `outside_temp` | outside temperature in °C | colder means more heating |
| `light` | sunlight in kilo-lux | more light means less heating |
| `humidity` | relative humidity in % | very dry or very humid air costs extra |
| `co2` | carbon dioxide in ppm | none. It is noise, and a good model learns to ignore it |
| `hour` | hour of the day, 0 to 23 | nights cost more |

The file `params.yaml` holds the numbers the generator uses:

```yaml
seed: 42        # the same seed always gives the same data
n_train: 2000   # rows for training
n_test: 500     # rows for testing
noise_std: 0.5  # how much random noise is added to energy
```

### 3. Generate the data in a temporary folder

Create a temporary folder for the dataset. Every command below uses it, so keep the shell open, or set `WORK` again in a new shell:

```bash
WORK=$(mktemp -d)
python generate.py "$WORK/greenhouse-export"
cp adapter.py "$WORK/greenhouse-export/"
```

`generate.py` writes 2,000 rows to `train.csv` and 500 rows to `test.csv` in `$WORK/greenhouse-export`, and the copy puts the adapter next to them. That folder is only the input of the next step. The repository is a sibling folder, `$WORK/greenhouse-data`, which `init` makes: it refuses a folder that already holds files.

The adapter declares two labels. `energy` is a `number` label: one finite number per sample. The five input columns are one `tabular` label: a dict of named columns, the same in every sample. The sample format section of `docs/datasets.md` in the CairnML SDK repository has the rules.

### 4. Set up the dataset and publish it to a private repository

The steps are separate commands. Everything up to `remote add` runs on your machine, and no remote is configured until you run `remote add`. First set the dataset up locally: `init` makes the git repository in the folder and records how `data/` is read, and the files and the adapter are copied in:

```bash
cairnml dataset init --path "$WORK/greenhouse-data" --adapter local
cp "$WORK/greenhouse-export/train.csv" "$WORK/greenhouse-export/test.csv" "$WORK/greenhouse-data/data/"
cp "$WORK/greenhouse-export/adapter.py" "$WORK/greenhouse-data/"
```

- `--adapter local` says that `adapter.py` at the top of the repository reads `data/`. It goes next to `data/`, not into it.
- `init` writes no storage and no remote: it does not reach GitHub or the server.

Create the private repository on GitHub, empty. Choose one way:

**Option A: with the GitHub command line** (`gh auth login` once):

```bash
gh repo create greenhouse-data --private
```

**Option B: in the browser.** Open [github.com/new](https://github.com/new), enter the name `greenhouse-data`, choose **Private**, leave **README**, **.gitignore** and **license** off, and click **Create repository**. The address is `https://github.com/<your-user>/greenhouse-data.git`.

Then list the credentials you can use, and note the id of your GitHub App from Example 3:

```bash
cairnml credential list
```

`cairnml credential list` shows each credential's id, type, name, scope (yours or the company's), owner and state.

Then connect the dataset to the repository with `remote add`, and name the credential:

```bash
cairnml dataset remote add https://github.com/<your-user>/greenhouse-data.git --credential <credential-id> --path "$WORK/greenhouse-data"
```

- The empty repository is the one you created above, under your account.
- `remote add` sets it as `origin`, chooses where the files are kept, and adds the dataset to the CairnML server with that credential. The server reads the dataset with that credential and no other. The storage is the dataset storage of your server, through DVC (the default). Add `--lfs` to keep the files in the GitHub LFS of the repository instead. The choice cannot be changed later.
- Without `--credential`, the dataset is public. Because this repository is private, `remote add` then warns you, and the dataset cannot be read until you add a credential with `cairnml dataset add-credential <credential-id>`.
- `remote add` then checks that the repository can be read with that credential. If it prints a warning that the repository is **not reachable with the credential**, stop here and do [step 6](#6-install-the-github-app-and-check-that-the-framework-sees-the-dataset) first: install the GitHub App on the repository, or choose another credential with `add-credential`. The warning does not undo the set-up.

`add`, `commit` and `push` refuse until `remote add` has run, so run them only after it.

Now record the files, check them, commit them and push:

```bash
cairnml dataset add --path "$WORK/greenhouse-data"
cairnml dataset commit --path "$WORK/greenhouse-data" -m "Add dataset"
cairnml dataset push --path "$WORK/greenhouse-data"
```

- `add` records `data/` and needs the storage, so `remote add` comes before it.
- `commit` checks the data against the adapter and commits it with its footprint. The first commit is `Add dataset`.
- `push` uploads the files, then publishes the commit to the empty repository.

After the push, protect the default branch by hand, so that changes come through pull requests. `cairnml dataset doctor --path "$WORK/greenhouse-data"` shows what is missing, and it is the same protection that `cairnml dataset create` sets up.

The command `cairnml dataset create` does all of this in one call, with the repository created for you. This example uses the separate commands so that each step is visible.

### 5. Look at the dataset repository

The dataset is a git repository with its commit. Look at the history and at the commit's files:

```bash
git -C "$WORK/greenhouse-data" log --oneline
git -C "$WORK/greenhouse-data" show --stat HEAD
```

You should see one commit, `Add dataset`. Git holds only the metadata: `adapter.py`, `dataset.yaml` (which says `adapter: local` and `storage: s3`), `dataset.lock.json` (the footprint, the record that the data was checked), `manifest.json`, `data.dvc` (the hash and size of the files in `data/`), `.gitignore` and the verify workflow. The CSV files are not in git. They are in the DVC storage of your server, and git holds only the pointer files that name them.

The SDK already ignores `data/` in git: `dvc add` writes `/data` to `.gitignore`, and `add` commits that line, so you add no rule of your own.

Record the two values that identify this version. The training code needs them:

```bash
REPO=$(git -C "$WORK/greenhouse-data" remote get-url origin)
COMMIT=$(git -C "$WORK/greenhouse-data" rev-parse HEAD)
echo "$REPO $COMMIT"
```

Keep them. The next examples take the repository URL and the commit as parameters, and they do not read any folder on your machine. You can delete `$WORK` when you are done: the repository and its data stay on GitHub and in the dataset storage.

### 6. Install the GitHub App and check that the framework sees the dataset

The server finds your datasets, and reads them for jobs, through the GitHub App you made in Example 3. It reads a repository only when the App is **installed on it**.

If `remote add` warned that the repository is not reachable with the credential, do this step before you run `push`. The checks below then pass.

1. On GitHub open **Settings → Applications → Installed GitHub Apps**, find your App and click **Configure**.
2. Under **Repository access**, choose **Only select repositories**, add `greenhouse-data` to the list, and click **Save**.

Then check that the dataset tools see the repository and its GitHub settings:

```bash
cairnml dataset doctor --path "$WORK/greenhouse-data"
```

`doctor` lists each check as `ok`, `FAIL` or `--`. It checks the set-up of the repository and the GitHub settings that publishing relies on. It does not check the App: that is checked in the web app, below.

To see the dataset as the framework sees it, open the **Datasets** page of your CairnML web app. The list shows `greenhouse-data`. Select it: the kind says **Your own dataset**, the repository is the URL from step 5, and the revision is the first characters of the commit from step 5. If the dataset is missing, the App is not installed on the repository yet, or the account you installed it on is not the one that owns the repository. Install it again on that account, then reload the page.

### 7. Read the dataset in training code

The training code reads one version of the dataset by its repository and commit. Pass the commit, not a branch, so you can rerun the same data later:

```bash
python read_dataset.py "$REPO" "$COMMIT"
```

`read_dataset.py` calls `Dataset.get`. It downloads the version into your cache, once, and records the repository, the commit and the content hash on the run. Then it runs `adapter.py` again into a temporary folder, reads each sample back with `Sample.label`, and logs the number of rows, and the mean and standard deviation of each column, per split. The labels are read back the same way the check wrote them: `energy` as a float, and the features as a dict of the five columns.

### 🔄 Changing the dataset later

A new version is a new commit. Change the files in `data/` of the dataset repository, then run `cairnml dataset add`, `cairnml dataset commit -m "message"` and `cairnml dataset push` with `--path "$WORK/greenhouse-data"`. `push` sends the files and opens a pull request into the protected default branch. Pass the new commit to the next examples to use the new version.

## 🔍 What to look for

- `dataset.yaml` says `adapter: local`, and `adapter.py` is at the top of the dataset repository, next to the `data/` folder.
- The run is in the project **examples**, task **greenhouse dataset read**. Its configuration lists the repository, the commit, the content hash and the storage of the dataset. The content hash is the hash in `data.dvc`.
- The `co2` column has no effect. In the next examples, a model that uses it will be no better than one that does not.

## 📄 Data

The data is generated by `generate.py`, from the seed in `params.yaml`. It is not based on any real measurements and carries no license restrictions.

## ➡️ Next steps

The next examples train models on this dataset. Each one needs the repository URL and the commit from this example. Continue with the [workflow pipeline example](../07-workflow-pipeline).
