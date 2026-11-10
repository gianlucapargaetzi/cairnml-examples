# Import a run from a project that does not use CairnML

## Goals

Bring a training run made **without** CairnML into the web app, by adapting its files to the import format.

What you will learn:

- What a CairnML import expects: a folder with a manifest, the settings, the per-epoch scalars and the checkpoints.
- How to write a small adapter that maps one project's names to CairnML's names.
- How to package the folder with `cairnml import prepare` and upload it in the web app.

## Background

This example brings a training run into CairnML that was made without CairnML. The run comes from a small "legacy" project: a plain training script that writes its own CSV log and its own checkpoint files. You will write an adapter that rearranges those files into the layout CairnML imports, and then import the run in the web app.

You do not need to change the legacy project to make this work. Everything the adapter needs is in the run folder.

## Before you start

- Time: about 10 minutes.
- [Example 6](../06-regression-dataset) is required. It created the dataset repository. Pass its repository URL and commit to this example: `--repo` and `--commit`.
- The SDK is installed, for `Dataset.get` and for the `cairnml import prepare` command. Building the ZIP does not need a server connection, but reading the dataset and the upload in step 7 do.

## Steps

### 1. Install the packages

```bash
cd examples/11-import-external-run
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 2. Look at the legacy project

Open `legacy_project/train_legacy.py`. It trains a small network on the greenhouse data, and for each run it writes a folder with four files:

```
runs/greenhouse_mlp_20261101_120000/
    settings.txt       the settings, one "name = value" per line
    log.csv            one row per epoch, with columns Epoch, Train Loss, Val Loss, Val R2
    model_final.pth    the weights after the last epoch
    model_best.pth     the weights of the epoch with the lowest validation loss
```

These names belong to this project only. CairnML does not know them, so it cannot read them as they are.

### 3. Run the legacy training

```bash
cd legacy_project
python train_legacy.py --repo https://github.com/<your-user>/greenhouse-data.git --commit <sha> --epochs 30
cd ..
```

The repository URL and the commit are the ones Example 6 recorded. The script reads `train.csv` and `test.csv` from the `data/` folder of that version, which `Dataset.get` downloads into your cache. Without `--repo` or `--commit` it stops with the message `run examples/06-regression-dataset first, then pass its dataset repository URL with --repo`, or the same for `--commit`.

The script prints the folder it wrote, for example `run written to runs/greenhouse_mlp_20261101_120000`. Its final line gives the best validation loss and the final R².

The legacy project runs without CairnML, so nothing is recorded on the server yet.

### 4. Compare the legacy names with CairnML's

CairnML imports a run folder with a fixed layout. Look at the table below, which is what the adapter does:

| Legacy file or column | CairnML name | What CairnML does with it |
|---|---|---|
| `settings.txt`, `name = value` | `args.yaml`, with `learning_rate`, `data_repository`, `data_commit` and similar | stored as parameters in the **Args** section of the task |
| `log.csv`, `Epoch` | `epoch` | the step of every scalar |
| `log.csv`, `Train Loss` | `loss/train` | the scalar **loss**, series **train** |
| `log.csv`, `Val Loss` | `loss/val` | the scalar **loss**, series **val** |
| `log.csv`, `Val R2` | `r2/val` | the scalar **r2**, series **val** |
| `model_final.pth`, `model_best.pth` | `weights/` | stored as model artifacts |

The column `Val R2` is the regression equivalent of accuracy. A classifier's accuracy is the share of correct answers. A regression model has no such share, so its score is the R², where 1.0 is a perfect fit and 0 is no better than predicting the average.

### 5. Export the run

Pass the run folder to the adapter:

```bash
python export_to_cairnml.py legacy_project/runs/greenhouse_mlp_20261101_120000 --project examples
```

The adapter does four things:

1. It reads `settings.txt` and `log.csv`, and renames the columns as in the table.
2. It copies the results into a scratch folder with the layout CairnML expects, next to a copy of `train_legacy.py` as `train.py`.
3. It runs `cairnml import prepare`, which packs the folder into one ZIP with a manifest.
4. It writes the ZIP to `exports/`.

The legacy folder is only read. Nothing in it changes.

The adapter names the new task after the run folder. To choose another name, pass `--task "greenhouse MLP (legacy)"`.

### 6. Check the ZIP

```bash
unzip -l exports/greenhouse_mlp_20261101_120000.zip
```

The archive has one top-level folder with:

- `cairnml-import.yaml`, the manifest, which says the project is `examples` and gives the task name
- `args.yaml`
- `results.csv`, with the columns `epoch`, `loss/train`, `loss/val` and `r2/val`
- `weights/model_final.pth` and `weights/model_best.pth`

You can open `results.csv` and check that it has one row per epoch.

### 7. Import the run in the web app

1. Open the web app and choose **Import run**.
2. Upload `exports/greenhouse_mlp_20261101_120000.zip`.
3. Open the task in project **examples**. It has the settings under **Configuration**, the three scalar curves under **Scalars**, and the two checkpoints under **Artifacts**.

Each import creates a new task. If you import the same ZIP twice, you get two tasks.

## What to look for

You end with an imported task with settings, curves and checkpoints.

- The legacy run uses the same data as the [baseline in Example 8](../08-hyperparameter-optimisation), with a different network and training loop. Compare their validation curves: the two should land in the same range.
- The `r2/val` curve approaches 1.0 but does not reach it, because of the noise in the data.
- The imported task can be compared with native runs. Choose both tasks in the web app and compare their curves.

## Troubleshooting

- **`missing columns`** when exporting: the legacy log does not have one of the four columns. Change the column names in `COLUMNS` in `export_to_cairnml.py` to the names your project uses.
- **`project is empty`** when preparing: add `--project examples`. The importer requires a project.
- **`no weights/ folder`** warning: the run has no checkpoint files, so no model is imported. The run still imports its scalars.

## Data

The data is generated by [Example 6](../06-regression-dataset). It is synthetic and carries no license restrictions.

## Next steps

Back to the [list of examples](../..). You have been through the whole path: tracking, private code, agents, datasets, workflows, searches, reports, the life of a task and imports.
