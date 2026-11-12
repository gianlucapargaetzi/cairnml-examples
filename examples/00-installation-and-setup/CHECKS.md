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
- [ ] `backend.user`: the new user exists (`name` = the username).
- [ ] `auth.device`: one document, `kind: "client"`, `revoked: false`, `user` = that user's id.
- [ ] `backend.share`: only the public `default` queue (`resource_type: "queue"`), no repository share.
- [ ] `task`, `project`, `repository`, `repository_assignment`, `registry_entry`, `user_access`: **0 documents**; `queue`: only `default`.

## FAIL signs
- The SDK comes from PyPI, or `cairnml repository` does not exist.
- A repository, task or project already exists on a fresh server.

## Result (2026-11-12, user testuser01, SDK and agent from the local checkouts)
- PASS: terminal (`cairnml init --device`, `cairnml devices list`, `cairnml repository list` empty), UI (empty Projects, empty Repositories & Datasets with the new empty state, Access empty, Devices lists the machine), DB (user, one client device, nothing else).
