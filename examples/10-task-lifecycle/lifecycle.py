"""Walk through the life of a task: create it, clone it, queue it, archive it, move it, publish it and delete it.

Each step is a subcommand, and you run them in order (see README.md). The script remembers the task IDs in state.json,
next to it, so the next step knows which task to act on.

    python lifecycle.py base                 # 1. create a finished task to work with
    python lifecycle.py clone --lr 0.1       # 2. copy it as a draft, with another learning rate
    python lifecycle.py enqueue              # 3. put the copy on a queue, so an agent can run it
    python lifecycle.py dequeue              #    take it back off the queue again
    python lifecycle.py reset --yes          # 4. remove the results of the copy, so it can run again
    python lifecycle.py archive              # 5. hide the copy from the task list
    python lifecycle.py unarchive            #    show it again
    python lifecycle.py move --project "examples scratch"   # 6. move it to another project
    python lifecycle.py publish --yes        # 7. publish the base task: read-only from now on
    python lifecycle.py delete --yes         # 8. delete the copy and its outputs
    python lifecycle.py status               # at any time: the state of both tasks
"""

import argparse
import json
from pathlib import Path

from cairnml import Task

PROJECT = "examples"
STATE = Path(__file__).resolve().parent / "state.json"
QUEUE = "default"


def load_state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2))


def task_of(state: dict, role: str) -> Task:
    """The task the state file holds for a role ("base" or "clone"). Stops with a hint if it is missing."""
    if role not in state:
        raise SystemExit(f"no {role} task yet: run the {'base' if role == 'base' else 'clone'} step first")
    return Task.get_task(task_id=state[role])


def describe(role: str, task: Task) -> None:
    print(f"{role}: {task.name} ({task.id}), status {task.get_status()}, project {task.get_project_name()}")


def need_yes(args: argparse.Namespace, what: str) -> None:
    """The steps that cannot be undone, or that remove results, only run with --yes."""
    if not args.yes:
        raise SystemExit(f"{what}. Run it again with --yes to confirm.")


def cmd_base(args, state):
    task = Task.init(project_name=PROJECT, task_name="lifecycle base", reuse_last_task_id=False)
    task.connect({"lr": 0.01, "hidden": 16})
    logger = task.get_logger()
    for step in range(5):
        logger.report_scalar("mse", "val", value=1.0 / (step + 1), iteration=step)
    task.close()
    state["base"] = task.id
    describe("base", task)


def cmd_clone(args, state):
    base = task_of(state, "base")
    # Clone creates a draft: a copy with the same code and settings, which you may still change.
    clone = Task.clone(source_task=base, name="lifecycle clone", project=PROJECT)
    clone.set_parameters_as_dict({"General": {"lr": args.lr}})
    state["clone"] = clone.id
    describe("clone", clone)


def cmd_enqueue(args, state):
    clone = task_of(state, "clone")
    Task.enqueue(clone, queue_name=QUEUE)
    describe("clone", clone)
    print(f"queued on '{QUEUE}'. No agent serves it (an agent serves only its own queue, example 4), so it stays queued.")


def cmd_dequeue(args, state):
    clone = task_of(state, "clone")
    Task.dequeue(clone)
    describe("clone", clone)


def cmd_reset(args, state):
    need_yes(args, "reset removes the results of the clone, which cannot be undone")
    clone = task_of(state, "clone")
    clone.reset(force=True)
    describe("clone", clone)


def cmd_archive(args, state):
    clone = task_of(state, "clone")
    clone.set_archived(True)
    print("archived: the clone is hidden from the task list. Use 'Open archive' in the web app to see it.")
    describe("clone", clone)


def cmd_unarchive(args, state):
    clone = task_of(state, "clone")
    clone.set_archived(False)
    describe("clone", clone)


def cmd_move(args, state):
    clone = task_of(state, "clone")
    clone.move_to_project(new_project_name=args.project)
    describe("clone", clone)


def cmd_publish(args, state):
    need_yes(args, "publishing makes the base task read-only, and it cannot be unpublished")
    base = task_of(state, "base")
    base.publish()
    describe("base", base)


def cmd_delete(args, state):
    need_yes(args, "delete removes the clone and its outputs, which cannot be undone")
    clone = task_of(state, "clone")
    clone.delete(delete_artifacts_and_models=True)
    state.pop("clone", None)
    print("deleted the clone and its outputs. The base task is untouched.")


def cmd_status(args, state):
    for role in ("base", "clone"):
        if role in state:
            describe(role, Task.get_task(task_id=state[role]))
        else:
            print(f"{role}: not created yet")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="step", required=True)
    commands = {
        "base": cmd_base, "clone": cmd_clone, "enqueue": cmd_enqueue, "dequeue": cmd_dequeue, "reset": cmd_reset,
        "archive": cmd_archive, "unarchive": cmd_unarchive, "move": cmd_move, "publish": cmd_publish,
        "delete": cmd_delete, "status": cmd_status,
    }
    for name in commands:
        p = sub.add_parser(name)
        p.add_argument("--yes", action="store_true", help="confirm a step that cannot be undone")
        if name == "clone":
            p.add_argument("--lr", type=float, default=0.1, help="the learning rate of the copy")
        if name == "move":
            p.add_argument("--project", required=True, help="the project to move the clone to")
    args = parser.parse_args()

    state = load_state()
    commands[args.step](args, state)
    save_state(state)


if __name__ == "__main__":
    main()
