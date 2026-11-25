# Checks: Example 1, hello world

## Terminal
- [ ] `python hello_world.py` ends with a line naming the seed and the task and exits 0; run it a second time with another seed and a changed line, as the README says.
- [ ] Two plain runs (`python hello_world.py`, no argument) print two different seeds in `done (seed N)`.
- [ ] Two runs with `python hello_world.py --seed 7` print `done (seed 7)` both times.

## UI
- [ ] Project **examples** exists and lists three tasks named **hello world** (the first run, the second run of step 3 and the changed run of step 4): all **Completed**, the last with seed 7 and the changed code line (compare shows the seed and the changed code line).
- [ ] While running, a task shows **Running** and a small progress bar for the `tqdm` bar `steps`, without a percentage logged.
- [ ] Task → **Configuration**: the seed parameter. Task → **Scalars**: a curve `loss` / `train`. Task → **Artifacts**: `hello`.
- [ ] Task → **Execution → Source code**: shows where the code ran from. If the examples checkout has a GitHub remote, the repository is listed there with an **Access** lock (green open for a public repository).
- [ ] **Compare** of the changed run and the first run shows the differing parameter and the differing code.
- [ ] **Compare** of the two plain runs: different `seed` under **Configuration** and visibly different noise in **Scalars**; Compare of the two `--seed 7` runs: the same `seed` and the `loss` / `train` curves equal point for point.
- [ ] **Repositories & Datasets**: if the checkout has a GitHub remote, **one** Code record for it (public: green open lock, no credential row but one empty row with the project **examples**); with no remote the list is still empty.

## Database
- [ ] `project`: one named `examples`, `user` = you.
- [ ] `task`: 3 documents (the README's three runs), `project` = examples, `status` completed, same `name`, differing `hyperparams`.
- [ ] `repository`: either 0 documents (no remote), or 1 with `roles: ["code"]`, `owner` = the **project owner** (you), `state: "ok"`; `share` has one `scope: "projects"` link from it to `examples`.
- [ ] No `repository_assignment` is needed for a public repository.

## FAIL signs
- A task is Completed but has no scalar or no artifact.
- A repository record exists although the examples were run in a folder without any Git remote.

## Result (2026-11-12)
- PASS: two `hello world` tasks, completed; the second has the 720-character uncommitted diff (`0.01` → `0.1`) and `seed` 7; Source code shows the repository and the commit.
- Found and fixed: the script started with noise `0.1`, so the README's "change 0.01 to 0.1" produced no diff. The script now starts at `0.01`.
- Observed: the examples checkout has a GitHub remote (public), so a **Code** record `cairnml-examples` is listed for `examples` (owner = project owner, share `inherited: true`); its Access lock is green open ("No credential assigned"), the Credentials table has one empty row, the trash is disabled.

## Result (2026-11-22, fresh stack, SDK from main plus the fixes of the same day)
- PASS: two runs without `--seed` recorded different seeds (517533234 and 1039215867) and different `loss` curves (sums 2.982 and 2.957); two runs with `--seed 7` recorded the same seed and identical curves (sum 2.943). `--seed 0` is honoured (checked with the stub probe).
- Before the change every run without `--seed` used seed 1571306751, because `Task.init` seeds the global generator with 1337.
