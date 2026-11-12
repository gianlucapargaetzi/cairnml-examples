# Checks: Example 8, hyperparameter optimisation

## Terminal
- [ ] `python baseline.py ...` prints `done: validation mse ...`; `python search.py --local ...` runs the trials and prints the best value; the `--queue` variant with `--concurrent 2` queues trials for the agent.

## UI
- [ ] Task **regression baseline** (Completed): **Configuration** lists `lr`, `hidden`, `batch_size`, `epochs`; its `mse` curve is there.
- [ ] Task **hyperparameter search**, type **optimizer**: lists the objective of every trial, best first; four trial tasks named after the base task, each with different parameters and a curve.
- [ ] On an agent: the trials run in the agent's queue, two at a time, and their source is the private repository with a green lock.
- [ ] Comparing the best and the worst trial shows different parameters (a very high learning rate makes the curve jump).

## Database
- [ ] `task`: the base task; one optimizer task (`type: "optimizer"`); N trial tasks whose `hyperparams` differ and which carry the base task as parent or origin; `status` completed.
- [ ] `repository`: unchanged (no duplicate for the dataset or the code repository).

## FAIL signs
- All trials have the same parameters; an optimizer task ends with no trial; a trial cannot read the dataset.
