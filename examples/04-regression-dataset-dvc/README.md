# A regression dataset in its own repository

This example builds a small dataset on your own machine, puts it in a dataset repository, and reads it back in training code. Nothing is downloaded: a script generates the data from a seed, so anyone who runs it gets the same files.

The problem is made up but reads like a real one. A small greenhouse uses energy to heat itself. Given the weather and the time of day, the model should predict how many kWh per hour it needs. You will use this dataset in the next examples.

## Features

- Generates two CSV files from a seed, so the same parameters always give the same data.
- Reads the CSV files through `adapter.py`, a local adapter in the dataset repository. The check runs it on your machine, and it checks every sample against the CairnML dataset format.
- Keeps the files in the dataset storage of your server, with DVC. The git history holds only the metadata.
- Reads the dataset in training code with `Dataset.get`, and records the repository, the commit and the content hash on the run.

## Prerequisites

- Python 3.9 or newer, and [git](https://git-scm.com).
- The [SDK connected to your server](../../README.md#prerequisites). The dataset storage is on the server, so `cairnml dataset init` needs the connection.
- A GitHub account, for the dataset repository in step 6.

## Step 1: Install the tools

Create a virtual environment and install the requirements:

```bash
cd examples/04-regression-dataset-dvc
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Check that the dataset commands are installed:

```bash
cairnml dataset --help
```

You should see the commands `init`, `add`, `check`, `commit` and `push`.

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

## Step 3: Create the dataset repository

The dataset lives in its own git repository, next to this example. Create the folder, set up git and the dataset storage:

```bash
mkdir ../greenhouse-data
git -C ../greenhouse-data init -b main
git -C ../greenhouse-data remote add origin https://github.com/<your-user>/greenhouse-data.git
cairnml dataset init --path ../greenhouse-data --adapter local
```

The remote is the repository you create on GitHub in step 6. It does not have to exist yet. `init` writes `dataset.yaml`, which says `adapter: local` (the adapter is `adapter.py` at the top of the repository) and `storage: s3`. The files are kept by DVC in the dataset storage of your server. Add `--storage lfs` to keep them in the GitHub LFS of the repository instead; the choice cannot be changed later.

## Step 4: Generate the data and add it

Generate the two files into the `data/` folder of the dataset repository, and copy the adapter next to `dataset.yaml`:

```bash
python generate.py ../greenhouse-data/data
cp adapter.py ../greenhouse-data/
```

`generate.py` writes 2,000 rows to `train.csv` and 500 rows to `test.csv`. Record the folder with the dataset tools, then check it:

```bash
cairnml dataset add --path ../greenhouse-data
cairnml dataset check --path ../greenhouse-data
```

`check` runs `adapter.py` on the CSV files and reports `The data passes` with 2500 samples. It writes `dataset.lock.json`, the footprint: the record that the data was checked, with the hash of the adapter.

The adapter declares two labels. `energy` is a `number` label: one finite number per sample. The five input columns are one `tabular` label: a dict of named columns, the same in every sample. The sample format section of `docs/datasets.md` in the CairnML SDK repository has the rules.

## Step 5: Commit the dataset

```bash
cairnml dataset commit --path ../greenhouse-data -m "Greenhouse dataset, seed 42"
```

`commit` checks the data again and commits it with its footprint. The commit is the version of the dataset. Git holds `data.dvc`, which lists the files in `data/` by their hash, and the metadata. The CSV files themselves are in the dataset storage.

Look at what the adapter is in the repository:

```bash
git -C ../greenhouse-data show --stat HEAD
```

## Step 6: Publish the dataset repository

This step needs GitHub and your server. First set up the GitHub command line, `gh`, and log in with `gh auth login`.

Create an empty private repository named `greenhouse-data` on GitHub, without a README or a `.gitignore`. Use the same address as the remote in step 3. For the demo, the owner installs the CairnML GitHub App on the account that owns this repository. Then check the GitHub settings and publish:

```bash
cairnml dataset doctor --path ../greenhouse-data
cairnml dataset push --path ../greenhouse-data
```

`doctor` lists each check as `ok`, `FAIL` or `--`, and tells you what to change on the repository's settings page for each failure. It only reads the settings. `push` sends the files to the dataset storage first, then the commit to the repository. It refuses a commit whose footprint does not hold.

## Step 7: Read the dataset in training code

The training code reads one version of the dataset by its repository and commit. Pass the commit, not a branch, so you can rerun the same data later:

```bash
COMMIT=$(git -C ../greenhouse-data rev-parse HEAD)
python read_dataset.py https://github.com/<your-user>/greenhouse-data.git $COMMIT
```

`read_dataset.py` calls `Dataset.get`. It downloads the version into your cache, once, and records the repository, the commit and the content hash on the run. Then it runs `adapter.py` again into a temporary folder, reads each sample back with `Sample.label`, and logs the number of rows, and the mean and standard deviation of each column, per split. The labels are read back the same way the check wrote them: `energy` as a float, and the features as a dict of the five columns.

## What to look for

- `dataset.yaml` says `adapter: local`, and `adapter.py` is at the top of the dataset repository, next to the `data/` folder.
- The run is in the project **examples**, task **greenhouse dataset read**. Its configuration lists the repository, the commit, the content hash and the storage of the dataset. The content hash is the hash in `data.dvc`.
- The `co2` column has no effect. In the next examples, a model that uses it will be no better than one that does not.

## Data

The data is generated by `generate.py`, from the seed in `params.yaml`. It is not based on any real measurements and carries no license restrictions.

## Next steps

The next examples train models on this dataset. Continue with the [hyperparameter optimisation example](../06-hyperparameter-optimisation).
