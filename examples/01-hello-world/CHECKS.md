# Checks: Example 1, hello world

## Terminal
- [ ] `python hello.py` ends with a line naming the task and exits 0; run it a second time with another seed and a changed line, as the README says.

## UI
- [ ] Project **examples** exists and lists two tasks named **hello world**: both **Completed**, one of them with a changed seed (compare shows the seed and the changed code line).
- [ ] While running, a task shows **Running** and a small progress bar for the `tqdm` bar `steps`, without a percentage logged.
- [ ] Task → **Configuration**: the seed parameter. Task → **Scalars**: a curve `loss` / `train`. Task → **Artifacts**: `hello`.
- [ ] Task → **Execution → Source code**: shows where the code ran from. If the examples checkout has a GitHub remote, the repository is listed there with an **Access** lock (green open for a public repository).
- [ ] **Compare** of the two tasks shows the differing parameter and the differing code.
- [ ] **Repositories & Datasets**: if the checkout has a GitHub remote, **one** Code record for it (public: green open lock, no credential row but one empty row with the project **examples**); with no remote the list is still empty.

## Database
- [ ] `project`: one named `examples`, `user` = you.
- [ ] `task`: 2 documents, `project` = examples, `status` completed, same `name`, differing `hyperparams`.
- [ ] `repository`: either 0 documents (no remote), or 1 with `roles: ["code"]`, `owner` = the **project owner** (you), `state: "ok"`; `share` has one `scope: "projects"` link from it to `examples`.
- [ ] No `repository_assignment` is needed for a public repository.

## FAIL signs
- A task is Completed but has no scalar or no artifact.
- A repository record exists although the examples were run in a folder without any Git remote.
