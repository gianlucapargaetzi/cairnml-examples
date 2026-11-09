"""Turn a run folder of the legacy project into a ZIP that CairnML can import.

The legacy project writes its own file names and column names (see legacy_project/train_legacy.py). CairnML imports a
run folder with a fixed layout:

    <run>/args.yaml     the settings, stored as parameters
    <run>/results.csv   one row per epoch; the epoch column is the step, and every other column is a scalar named
                        "metric/series", for example "loss/train"
    <run>/weights/      the checkpoints, stored as model artifacts

This script reads the legacy folder, renames what needs renaming, copies the files into that layout and then runs
`cairnml import prepare`, which packs the folder into one ZIP with a manifest. Nothing in the legacy folder is changed.

    python export_to_cairnml.py legacy_project/runs/<run> --project examples
"""

import argparse
import csv
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TRAIN_SCRIPT = HERE / "legacy_project" / "train_legacy.py"
# The legacy column names, and the names CairnML expects. The epoch column becomes the step of every scalar.
COLUMNS = {"Epoch": "epoch", "Train Loss": "loss/train", "Val Loss": "loss/val", "Val R2": "r2/val"}
CHECKPOINTS = ["model_final.pth", "model_best.pth"]


def read_settings(path: Path) -> dict:
    """The legacy settings file: one "name = value" per line. Names become keys with underscores, for example
    "learning rate" becomes "learning_rate"."""
    settings = {}
    for line in path.read_text().splitlines():
        if "=" in line:
            name, _, value = line.partition("=")
            settings[name.strip().replace(" ", "_")] = value.strip()
    return settings


def read_log(path: Path) -> list:
    """The legacy log with the columns renamed. Stops with a clear message if a column is missing."""
    with open(path, newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"{path.name}: missing columns {missing}; this export knows {list(COLUMNS)}")
        return [{COLUMNS[column]: row[column] for column in COLUMNS} for row in reader]


def write_csv(path: Path, rows: list) -> None:
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(COLUMNS.values()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", type=Path, help="the run folder of the legacy project")
    parser.add_argument("--project", required=True, help="the CairnML project to import into")
    parser.add_argument("--task", help="the name of the new task (default: the run folder name)")
    parser.add_argument("--output", type=Path, default=HERE / "exports", help="folder for the ZIP")
    args = parser.parse_args()

    run = args.run.resolve()
    if not run.is_dir():
        raise SystemExit(f"not a run folder: {run}")
    task_name = args.task or run.name
    rows = read_log(run / "log.csv")
    settings = read_settings(run / "settings.txt")

    # Build the layout in a scratch folder: the legacy folder itself is only read.
    with tempfile.TemporaryDirectory(prefix="legacy-export-") as scratch:
        staged = Path(scratch) / run.name
        (staged / "weights").mkdir(parents=True)
        (staged / "args.yaml").write_text(yaml.safe_dump(settings, sort_keys=False))
        write_csv(staged / "results.csv", rows)
        for name in CHECKPOINTS:
            if (run / name).is_file():
                shutil.copy2(run / name, staged / "weights" / name)
        # The importer looks for the training script at or above the run folder, so it goes next to the run folder.
        shutil.copy2(TRAIN_SCRIPT, Path(scratch) / "train.py")

        args.output.mkdir(parents=True, exist_ok=True)
        zip_path = args.output / f"{run.name}.zip"
        command = [sys.executable, "-m", "cairnml.cli", "import", "prepare", str(staged),
                   "--project", args.project, "--task", task_name, "--output", str(zip_path), "--force"]
        print("running:", " ".join(command))
        subprocess.run(command, check=True)

    print(f"done: {zip_path}")
    print("next: in the web app, open Import run and upload this ZIP.")


if __name__ == "__main__":
    main()
