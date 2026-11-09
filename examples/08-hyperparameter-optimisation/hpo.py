"""Search the hyperparameters of train_regression.py with Optuna.

Optuna only proposes values and reads the results, so this controller runs on any machine with a CPU. Each trial is a
copy of the base task with new values, and it runs on the queue you name. The trials are the expensive part, so that
queue is the one with a GPU agent on it.

    python hpo.py --base-task-id <id> --queue gpu --trials 20   # trials run on the agents of the 'gpu' queue
    python hpo.py --base-task-id <id> --local --trials 4         # trials run on this machine, to try it out

The base task id is printed at the end of a run of train_regression.py, and shown in the web app.
"""

import argparse

from cairnml import Task
from cairnml.automation import (
    DiscreteParameterRange,
    HyperParameterOptimizer,
    LogUniformParameterRange,
    UniformIntegerParameterRange,
)
from cairnml.automation.optuna import OptimizerOptuna

EPOCHS_PER_TRIAL = 30


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-task-id", required=True, help="the task that train_regression.py created")
    parser.add_argument("--trials", type=int, default=20, help="how many trials to run in total")
    parser.add_argument("--concurrent", type=int, default=2, help="how many trials run at the same time")
    parser.add_argument("--queue", default="default", help="the queue whose agents run the trials")
    parser.add_argument("--local", action="store_true", help="run the trials on this machine instead of an agent")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    # The search itself is a task of type optimizer, so it shows up in the web app with its trials.
    task = Task.init(project_name="examples", task_name="hyperparameter search", task_type=Task.TaskTypes.optimizer)

    optimizer = HyperParameterOptimizer(
        base_task_id=args.base_task_id,
        hyper_parameters=[
            LogUniformParameterRange("General/lr", min_value=-4, max_value=-1),
            UniformIntegerParameterRange("General/hidden", min_value=8, max_value=128),
            DiscreteParameterRange("General/batch_size", values=[16, 32, 64, 128]),
        ],
        # Minimise the validation mean squared error at the last epoch.
        objective_metric_title="mse",
        objective_metric_series="val",
        objective_metric_sign="min",
        optimizer_class=OptimizerOptuna,
        max_number_of_concurrent_tasks=args.concurrent,
        execution_queue=args.queue,
        # Passed on to Optuna: each trial may run EPOCHS_PER_TRIAL reports, and the search stops after --trials trials.
        max_iteration_per_job=EPOCHS_PER_TRIAL,
        total_max_jobs=args.trials,
    )

    if args.local:
        optimizer.start_locally()
    else:
        optimizer.start()
    optimizer.wait()
    optimizer.stop()

    for trial in optimizer.get_top_experiments(top_k=3):
        print(f"top trial {trial.id}: {trial.name}")
    task.close()


if __name__ == "__main__":
    main()
