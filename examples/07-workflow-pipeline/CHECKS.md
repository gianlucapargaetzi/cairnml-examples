# Checks: Example 7, a workflow

## Terminal
- [ ] `python pipeline.py --repo <REPO> --commit <COMMIT>` runs the three steps on this machine and ends; with the agent queue (step 5) the steps are queued and the daemon runs them.

## UI
- [ ] Project **examples**: the run **greenhouse workflow** with a graph `prepare_data → train → evaluate`; each box opens its own task; all **Completed**.
- [ ] `train` shows the validation error, `evaluate` the R²; a second run with another `--lr` gives a second pair of `train` tasks to compare.
- [ ] **Repositories & Datasets**: `greenhouse-data` lists a second run in its **Runs** tab; the credentials table still has your App, now with `examples` and a newer **Last used** after the agent ran the steps.
- [ ] On an agent: steps show their queue, run on this machine, and clone the private dataset repository with a read token (green lock, no extra credential).

## Database
- [ ] `task`: one controller (pipeline) task and three step tasks with `parent` = the controller; `type` of the controller is controller; steps completed.
- [ ] `repository_assignment.last_used` updated after the agent steps; no new `repository` record for `greenhouse-data`.

## FAIL signs
- A step runs but cannot read the dataset (token refused); the steps run in another project.
