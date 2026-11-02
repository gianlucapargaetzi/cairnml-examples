"""Read the greenhouse dataset from its dataset repository and record it with the run.

    python read_dataset.py <repository> <commit>

Dataset.get downloads one version of the dataset into the cache, once, and records the repository, the commit and the
content hash on the task. The run therefore shows which data it used. Pass a commit, not a branch, to rerun the same
data later. The repository can be a URL or the path of a local clone.

The labels come from the adapter in the repository: the adapter runs again here, into a temporary folder, and each
sample is read back with Sample.label. The energy is a float and the features are a dict of the five columns.
"""

import argparse
import tempfile
from pathlib import Path

import pandas as pd

from cairnml import Task
from cairnml.datasets import Dataset, ExternalDataset, SampleWriter
from cairnml.datasets.external import load_local_adapter


def read_samples(data: Dataset):
    """The (split, features, energy) of every sample, as the adapter writes them."""
    adapter = load_local_adapter(data.path.parent / "adapter.py")
    with tempfile.TemporaryDirectory() as out:
        writer = SampleWriter(Path(out), dict(adapter.modalities), dict(adapter.labels), source_root=data.path)
        adapter.run(data.path, writer)
        writer.close()
        table = ExternalDataset({"name": "greenhouse"}, Path(out), data.path)
        return [(sample.split, sample.label("features"), sample.label("energy")) for sample in table.samples()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Read the greenhouse dataset and record it with a run.")
    parser.add_argument("repository", help="URL of the dataset repository, or the path of a local clone")
    parser.add_argument("commit", help="commit of the dataset repository")
    args = parser.parse_args()

    task = Task.init(project_name="examples", task_name="greenhouse dataset read")
    data = Dataset.get(args.repository, args.commit)
    print(f"dataset {data.repo} at {data.commit[:10]}, content {data.content_hash}, files in {data.path}")

    samples = read_samples(data)
    first_split, first_features, first_energy = samples[0]
    print(f"read {len(samples)} samples; first sample ({first_split}): energy {first_energy!r} "
          f"({type(first_energy).__name__}), features {sorted(first_features)}")

    frame = pd.DataFrame([{"split": split, **features, "energy": energy} for split, features, energy in samples])
    columns = [column for column in frame.columns if column != "split"]
    logger = task.get_logger()
    for split in ("train", "test"):
        part = frame[frame["split"] == split]
        logger.report_scalar("rows", split, value=len(part), iteration=0)
        for column in columns:
            logger.report_scalar(f"mean {column}", split, value=float(part[column].mean()), iteration=0)
            logger.report_scalar(f"std {column}", split, value=float(part[column].std()), iteration=0)
    task.close()
    print("done: the run is in the web app, project 'examples', task 'greenhouse dataset read'")


if __name__ == "__main__":
    main()
