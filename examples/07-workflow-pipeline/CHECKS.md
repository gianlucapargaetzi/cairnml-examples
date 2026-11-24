# Checks: Example 7, a workflow

## Terminal
- [ ] `python pipeline.py --repo <REPO> --commit <COMMIT>` runs the three steps on this machine and ends; with the agent queue (step 5) the steps are queued and the daemon runs them.

## UI
- [ ] Project **examples**: the run **greenhouse workflow** with a graph `prepare_data → train → evaluate`; each box opens its own task; all **Completed**.
- [ ] `train` shows the validation error and `evaluate` the R², as `val_mse` and `test_r2` under **Configuration → return**; a second run with another `--lr` gives a second pair of `train` tasks to compare.
- [ ] **Repositories & Datasets**: `greenhouse-data` lists a second run in its **Runs** tab; the credentials table still has your App, now with `examples` and a newer **Last used** after the agent ran the steps.
- [ ] On an agent: steps show their queue, run on this machine, and clone the private dataset repository with a read token (green lock, no extra credential).
- [ ] On an agent: each step's **Configuration → Installed packages** lists what `pipeline.py` names in `packages=`: `prepare_data` lists `cairnml[dataset]`; `train` and `evaluate` list `torch` and `pandas`.

## Database
- [ ] `task`: one controller (pipeline) task and three step tasks with `parent` = the controller; `type` of the controller is controller; steps completed.
- [ ] `repository_assignment.last_used` updated after the agent steps; no new `repository` record for `greenhouse-data`.

## FAIL signs
- A step runs but cannot read the dataset (token refused); the steps run in another project.
- On an agent, a step fails with `No module named 'torch'` (or `dvc`): its packages were not installed, check the step's **Installed packages** and the `packages=` of its component.

## Result (2026-11-12, fresh stack)
PASS, with a second worker. Local run: `workflow done: validation mse 0.3095, test R2 0.9812`. Agent run (`--queue <agent queue>`): the controller runs in the terminal, the three steps run on the agent; `workflow done: validation mse 0.3413, test R2 0.9793`. All four tasks Completed; steps have the controller as parent.

Needed for the agent run (found by running it):
- The controller must not run on the same single worker as its steps (it blocks them): it runs where it is started (`pipeline_execution_queue=None`), and a second worker on the queue is useful (`CAIRNML_WORKER_ID=<machine>:1 cairnml-agent daemon --docker`).
- A step reads the step before it (a sibling task) and downloads its artifact: the server lets a job read the data of the steps of its own pipeline (same parent), nothing else.
- The steps pass the weights themselves, not a file path (the next step may run on another machine).
Not verified yet: starting a pipeline from the web app (controller as a job on an agent), and the "Pipeline dead-locked" message, which has unit tests only.

## Result (2026-11-22, fresh stack, agent from source with `daemon --docker python:3.12-slim`, SDK from main plus the fixes of the same day)
- PASS with the steps naming their packages: agent run (`--queue <agent queue>`) `workflow done: validation mse 0.3095, test R2 0.9812`, also when the controller's environment has no `pigar`; `--local` run: the same line.
- The example without `packages=` failed on the agent in BOTH environments: without `pigar` the SDK logs "Failed auto-generating package requirements" for each step and the `train` step dies with `No module named 'torch'`; with `pigar` installed the SDK recorded only `cairnml == 0.0.9` for the `train` step (no warning), and `train` died the same way. So the imports inside a step function are not detected (an SDK defect, filed separately), and the example names its packages.
