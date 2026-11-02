# A regression dataset in its own repository

This example builds a small dataset on your own machine, publishes it as a private dataset repository, and reads it back in training code. Nothing is downloaded from the internet: a script generates the data from a seed, so anyone who runs it gets the same files.

The problem is made up but reads like a real one. A small greenhouse uses energy to heat itself. Given the weather and the time of day, the model should predict how many kWh per hour it needs. You will use this dataset in the next examples. They read it from the repository and commit that this example creates.

## Features

- Generates two CSV files from a seed, so the same parameters always give the same data.
- Reads the CSV files through `adapter.py`, a local adapter in the dataset repository. The check runs it on your machine, and it checks every sample against the CairnML dataset format.
- Creates a **private** dataset repository on GitHub with one command, and keeps the files in the dataset storage of your server, with DVC. The git history holds only the metadata.
- Makes the repository visible to the framework through the CairnML GitHub App, so the server can read it for jobs and list it.
- Reads one version of the dataset in training code with `Dataset.get`, and records the repository, the commit and the content hash on the run.

## Prerequisites

- Python 3.9 or newer, and [git](https://git-scm.com).
- The [SDK connected to your server](../../README.md#prerequisites). The dataset storage is on the server, so `cairnml dataset create` needs the connection.
- The [GitHub command line](https://cli.github.com), `gh`, logged in with `gh auth login`. The dataset repository is created with it, under your GitHub account.
- The CairnML GitHub App link from your server operator. See step 6.

## Step 1: Install the tools

Create a virtual environment and install the requirements:

```bash
cd examples/04-regression-dataset
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Check that the dataset commands are installed:

```bash
cairnml dataset --help
```

You should see the commands `create`, `doctor`, `get` and `commit`, among others.

## Step 2: Look at the generator

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

## Step 3: Generate the data

The dataset repository is created from a folder of files. Generate the two CSV files into a folder next to this example, and copy the adapter next to them:

```bash
python generate.py ../greenhouse-export
cp adapter.py ../greenhouse-export/
```

`generate.py` writes 2,000 rows to `train.csv` and 500 rows to `test.csv`. The adapter has to be in the folder too: `adapter.py` is the adapter of the dataset, and the create command moves it to the top of the repository, next to `dataset.yaml`, while the CSV files go to `data/`.

The adapter declares two labels. `energy` is a `number` label: one finite number per sample. The five input columns are one `tabular` label: a dict of named columns, the same in every sample. The sample format section of `docs/datasets.md` in the CairnML SDK repository has the rules.

## Step 4: Create the private dataset repository

One command creates the repository on GitHub, copies the files in, checks them, commits them with their footprint, pushes, and protects the default branch:

```bash
cairnml dataset create greenhouse-data --from ../greenhouse-export --adapter local --storage s3 --path ../greenhouse-data
```

- `greenhouse-data` is the name of the new GitHub repository. It is created **private** by default; the flag `--public` would make it public, and you do not need it.
- `--from` is the folder from step 3, and `--adapter local` says that its `adapter.py` is the adapter.
- `--storage s3` keeps the files in the dataset storage of your server, through DVC. Use `--storage lfs` to keep them in the GitHub LFS of the repository instead. The choice cannot be changed later.
- `--path` is the local folder that holds the repository. Only the command uses it: the examples that follow read the repository by its URL and commit, not from this folder.

The command prints the address of the repository, `https://github.com/<your-user>/greenhouse-data.git`, and the first commit. If it warns that the branch is not protected, protect it by hand; `cairnml dataset doctor` shows what is missing.

## Step 5: Look at the dataset repository

The dataset is a git repository with its commit. Look at the history and at the commit's files:

```bash
git -C ../greenhouse-data log --oneline
git -C ../greenhouse-data show --stat HEAD
```

You should see one commit, `Add dataset`. Its files are `adapter.py`, `dataset.yaml` (which says `adapter: local` and `storage: s3`), `dataset.lock.json` (the footprint, the record that the data was checked), `data.dvc` (which lists the files in `data/` by their hash), and the `data/` folder. The CSV files themselves are in the dataset storage, and git holds their hashes.

Record the two values that identify this version. The training code needs them:

```bash
REPO=$(git -C ../greenhouse-data remote get-url origin)
COMMIT=$(git -C ../greenhouse-data rev-parse HEAD)
echo "$REPO $COMMIT"
```

Keep them. The next examples take the repository URL and the commit as parameters, and they do not read any folder on your machine.

## Step 6: Install the CairnML GitHub App and check that the framework sees the dataset

The server reads a private repository through the CairnML GitHub App. The server finds your datasets through the same App, so the repository is listed and can be read for jobs only once the App is installed on it.

1. Get the App link from your server operator, `<App link from your CairnML server's README>`. Your CairnML server's README describes the App; the link is the one for your server.
2. Open the link and install the App on the GitHub account that owns the repository: the account you logged in with `gh auth login`.
3. Select the repository `greenhouse-data` and confirm.

Then check, from this example folder, that the dataset tools see the repository and its GitHub settings:

```bash
cairnml dataset doctor --path ../greenhouse-data
```

`doctor` lists each check as `ok`, `FAIL` or `--`. It checks the set-up of the repository and the GitHub settings that publishing relies on. It does not check the App: that is checked in the web app, below.

To see the dataset as the framework sees it, open the **Datasets** page of your CairnML web app. The list shows `greenhouse-data`. Select it: the kind says **Your own dataset**, the repository is the URL from step 5, and the revision is the first characters of the commit from step 5. If the dataset is missing, the App is not installed on the repository yet, or the account you installed it on is not the one that owns the repository. Install it again on that account, then reload the page.

## Step 7: Read the dataset in training code

The training code reads one version of the dataset by its repository and commit. Pass the commit, not a branch, so you can rerun the same data later:

```bash
python read_dataset.py $REPO $COMMIT
```

`read_dataset.py` calls `Dataset.get`. It downloads the version into your cache, once, and records the repository, the commit and the content hash on the run. Then it runs `adapter.py` again into a temporary folder, reads each sample back with `Sample.label`, and logs the number of rows, and the mean and standard deviation of each column, per split. The labels are read back the same way the check wrote them: `energy` as a float, and the features as a dict of the five columns.

## Changing the dataset later

A new version is a new commit. Change the files in `data/` of the dataset repository, then run `cairnml dataset add`, `cairnml dataset commit -m "message"` and `cairnml dataset push` in that repository. `push` sends the files and opens a pull request into the protected default branch. Pass the new commit to the next examples to use the new version.

## What to look for

- `dataset.yaml` says `adapter: local`, and `adapter.py` is at the top of the dataset repository, next to the `data/` folder.
- The run is in the project **examples**, task **greenhouse dataset read**. Its configuration lists the repository, the commit, the content hash and the storage of the dataset. The content hash is the hash in `data.dvc`.
- The `co2` column has no effect. In the next examples, a model that uses it will be no better than one that does not.

## Data

The data is generated by `generate.py`, from the seed in `params.yaml`. It is not based on any real measurements and carries no license restrictions.

## Next steps

The next examples train models on this dataset. Each one needs the repository URL and the commit from this example. Continue with the [workflow pipeline example](../05-workflow-pipeline).
