"""Hello, CairnML: one run with parameters, a metric curve and an artifact."""

from pathlib import Path

from cairnml import Task

task = Task.init(project_name="examples", task_name="hello world")
settings = task.connect({"greeting": "Hello, CairnML!", "steps": 10})

logger = task.get_logger()
for step in range(settings["steps"]):
    logger.report_scalar(title="loss", series="train", value=1.0 / (step + 1), iteration=step)

Path("hello.txt").write_text(settings["greeting"] + "\n")
task.upload_artifact("hello", artifact_object="hello.txt")
task.close()
print("done: the run is in the web app, project 'examples', task 'hello world'")
