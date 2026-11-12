# Checks: Example 0, installation and setup

## Terminal
- [ ] `pip show cairnml cairnml-agent` shows the **editable local checkouts** (see `../CHECKS.md`), not PyPI.
- [ ] `cairnml --help` lists `repository`, `dataset`, `credential`, `devices`; `cairnml repository --help` lists `list, add, assign, unassign, check, delete, unshare, share, link, unlink`.
- [ ] `cairnml init http://<server>` and the enrolment finish without an error; `cairnml devices list` shows this machine, kind client, not revoked.
- [ ] `cairnml repository list` prints "No repositories yet" (nothing was run).

## UI
- [ ] Sign-in with the new user opens **Projects**, empty.
- [ ] Side bar: Projects, Pipelines, **Repositories & Datasets**, Agents & Queues (no "Datasets" tab of the old design).
- [ ] **Repositories & Datasets** shows the empty state "No repositories or datasets yet".
- [ ] **Settings → Access** is empty. **Settings → Devices** lists this machine, kind **Client**.

## Database
- [ ] `user`: the new user exists, `role` is `user` (only the admin account has `admin`).
- [ ] `device`: one document, `kind` client, `revoked: false`, owned by that user.
- [ ] `task`, `project`, `repository`, `repository_assignment`, `registry_entry`, `user_access`: **0 documents**.

## FAIL signs
- The SDK comes from PyPI, or `cairnml repository` does not exist.
- A repository, task or project already exists on a fresh server.
