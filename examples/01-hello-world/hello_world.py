"""Hello, CairnML: one run with parameters, a metric curve and an artifact."""

import argparse
import random
from pathlib import Path

from tqdm import tqdm

from cairnml import Task

parser = argparse.ArgumentParser(description="Hello, CairnML example run.")
parser.add_argument("--seed", type=int, default=None,
                    help="random seed for the noise; a random seed is chosen if omitted")
args = parser.parse_args()

task = Task.init(project_name="examples", task_name="hello world")

seed = args.seed if args.seed is not None else random.randrange(2**31)
settings = task.connect({"greeting": "Hello, CairnML!", "steps": 10, "seed": seed})
seed = settings["seed"]

rng = random.Random(seed)
logger = task.get_logger()
# logger.report_scalar(title="seed", series="seed", value=seed, iteration=0)

for step in tqdm(range(settings["steps"]), desc="steps", unit="step"):
    loss = 1.0 / (step + 1) + rng.gauss(0.0, 0.1)  # slight noise so runs differ
    logger.report_scalar(title="loss", series="train", value=loss, iteration=step)

Path("hello.txt").write_text(settings["greeting"] + "\n")
task.upload_artifact("hello", artifact_object="hello.txt")
task.close()
print(f"done (seed {seed}): the run is in the web app, project 'examples', task 'hello world'")
