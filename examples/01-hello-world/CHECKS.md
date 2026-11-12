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

## Result (2026-11-12)
- PASS: two `hello world` tasks, completed; the second has the 720-character uncommitted diff (`0.01` → `0.1`) and `seed` 7; Source code shows the repository and the commit.
- Found and fixed: the script started with noise `0.1`, so the README's "change 0.01 to 0.1" produced no diff. The script now starts at `0.01`.
- Observed: the examples checkout has a GitHub remote (public), so a **Code** record `cairnml-examples` is listed for `examples` (owner = project owner, share `inherited: true`); its Access lock is green open ("No credential assigned"), the Credentials table has one empty row, the trash is disabled.
