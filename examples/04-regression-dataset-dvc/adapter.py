"""The adapter of the greenhouse dataset: reads data/train.csv and data/test.csv, one sample per row.

It goes to the top of the dataset repository, next to dataset.yaml (adapter: local). `cairnml dataset check` runs it and
checks every sample against the standard format. The training code reads the CSV files directly.

Each sample names the CSV file its row comes from (the table modality). The target is a number label, and the five input
columns are one tabular label: a dict of named columns.
"""

import csv

from cairnml.datasets import Adapter

FEATURES = ["outside_temp", "light", "humidity", "co2", "hour"]
TARGET = "energy"
SPLITS = ["train", "test"]


class GreenhouseCsv(Adapter):
    modalities = {"table": "table"}
    labels = {"features": "tabular", "energy": "number"}

    def run(self, source, writer):
        for split in SPLITS:
            file_name = f"{split}.csv"
            with open(source / file_name, newline="") as handle:
                for number, row in enumerate(csv.DictReader(handle), start=1):
                    features = {name: float(row[name]) for name in FEATURES}
                    writer.add(
                        f"{split}-{number:05d}",
                        split,
                        {"table": file_name},
                        {"features": features, "energy": float(row[TARGET])},
                    )
