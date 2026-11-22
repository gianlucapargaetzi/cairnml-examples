# Checks: Example 0, installation and setup

## Terminal
- [ ] `pip show cairnml cairnml-agent` shows the **editable local checkouts** (see `../CHECKS.md`), not PyPI.
- [ ] `cairnml --help` lists `repository`, `dataset`, `credential`, `devices`; `cairnml repository --help` lists `list, add, assign, unassign, check, delete, unshare, share, link, unlink`.
- [ ] `cairnml init http://<server>` and the enrolment finish without an error; `cairnml devices list` shows this machine, kind client, not revoked.
- [ ] `cairnml repository list` prints "No repositories yet" (nothing was run).

## UI
- [ ] Sign-in with the new user opens the **Dashboard** (heading **Projects**): **Recent projects**, **Recent reports**, **Recent tasks** empty; **Welcome to CairnML** and **What's new** dialogs close with the **X** and **Dismiss**.
- [ ] Side bar: icons only, top to bottom Agents & Queues, Datasets, Projects, Pipelines; the names are tooltips; the **Datasets** icon opens **Repositories & Datasets**.
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

## Result (2026-11-22, README wording)
- The sign-in page, the icon-only sidebar, the Dashboard with the welcome and What's new dialogs, the "+" Add credential button, Task actions (Clone, Enqueue) and the Import dialog were observed on 2026-11-21 on the same web build (cairnml-web 21228b9) with screenshots; the General-versus-Args statement of Example 4 was run on 2026-11-22: a clone with only `Args/epochs` changed ran 1 epoch, one with only `General/epochs` changed ran 2 epochs. `cairnml-agent daemon --help` lists `--gpus` and `--cpu-only`.
