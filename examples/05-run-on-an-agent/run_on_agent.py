"""Hello, CairnML on an agent: the hello world run, executed on a machine running cairnml-agent."""

from pathlib import Path

from cairnml import Task

task = Task.init(project_name="examples", task_name="run on an agent")
# Queue the task for an agent on the 'default' queue. This process exits here; the agent
# runs the script again from the start, and the rest of the script runs on the agent.
task.execute_remotely(queue_name="default")

settings = task.connect({"greeting": "Hello from an agent!", "steps": 10})

logger = task.get_logger()
for step in range(settings["steps"]):
    logger.report_scalar(title="loss", series="train", value=1.0 / (step + 1), iteration=step)

Path("hello.txt").write_text(settings["greeting"] + "\n")
task.upload_artifact("hello", artifact_object="hello.txt")
task.close()
print("done: the run is in the web app, project 'examples', task 'run on an agent'")
