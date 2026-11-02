"""Generate the greenhouse energy dataset: a regression problem with five input columns and one target column.

The target is the heating energy of a small greenhouse in kWh per hour. It depends on the outside temperature (colder
means more heating), the sunlight (more light means less heating), the humidity (both very dry and very humid air cost
extra energy) and the time of day (nights cost more). The carbon dioxide column is pure noise: a model should learn to
ignore it. Everything is drawn from one seed, so the same parameters always give the same files.

Run it from this folder. It reads params.yaml and writes train.csv and test.csv into the output folder, which is data/
if you do not give one:

    python generate.py ../greenhouse-export
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

PARAMS = Path("params.yaml")


def make_split(rng: np.random.Generator, rows: int, noise_std: float) -> pd.DataFrame:
    """One split of rows samples. Each column is drawn from a range that looks like a real greenhouse."""
    outside_temp = rng.uniform(-5.0, 25.0, rows)          # degrees Celsius
    light = rng.uniform(0.0, 100.0, rows)                 # kilo-lux
    humidity = rng.uniform(30.0, 95.0, rows)              # percent
    co2 = rng.uniform(400.0, 1200.0, rows)                # parts per million, no effect on the target
    hour = rng.integers(0, 24, rows).astype(float)        # hour of the day

    energy = (
        12.0
        - 0.35 * outside_temp
        - 0.08 * light
        + 0.0015 * (humidity - 60.0) ** 2
        + 1.5 * np.cos(2 * np.pi * hour / 24)
        + rng.normal(0.0, noise_std, rows)
    )
    return pd.DataFrame({
        "outside_temp": outside_temp,
        "light": light,
        "humidity": humidity,
        "co2": co2,
        "hour": hour,
        "energy": energy,
    }).round(4)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the greenhouse energy dataset as two CSV files.")
    parser.add_argument("output", nargs="?", default="data", type=Path, help="folder for train.csv and test.csv")
    output = parser.parse_args().output
    params = yaml.safe_load(PARAMS.read_text())
    rng = np.random.default_rng(params["seed"])
    output.mkdir(parents=True, exist_ok=True)
    train = make_split(rng, params["n_train"], params["noise_std"])
    test = make_split(rng, params["n_test"], params["noise_std"])
    train.to_csv(output / "train.csv", index=False)
    test.to_csv(output / "test.csv", index=False)
    print(f"wrote {len(train)} training rows and {len(test)} test rows to {output}/")


if __name__ == "__main__":
    main()
