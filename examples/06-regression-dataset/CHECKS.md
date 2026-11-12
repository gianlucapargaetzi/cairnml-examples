# Checks: Example 6, a dataset of your own

Needs the GitHub App installed on the **new** repository `greenhouse-data` (step 4, by hand).

## Terminal
- [ ] Before the push: the App has Contents and Workflows **write** and the installation accepted them. With a read-only App the push is refused with the reason (FAIL of the example, not of CairnML: fix the App and repeat).
- [ ] `cairnml dataset --help` lists `init, remote, clone, status, add, check, commit, doctor, push, get, create, list, cache`.
- [ ] `cairnml dataset remote add <url> --credential <id>` sets origin and the storage, lists the dataset and does **not** warn about reachability.
- [ ] `cairnml dataset add`, `commit` and `push` succeed; `cairnml dataset doctor` reports nothing missing (after "Allow auto-merge" and branch protection on `main` are on; the first push goes straight to `main`); `cairnml dataset check` passes.
- [ ] `cairnml dataset list` and `cairnml repository list --type dataset` show `greenhouse-data`, READ AS `credential`.
- [ ] `REPO` and `COMMIT` are noted for Examples 7 to 11.

## UI
- [ ] **Repositories & Datasets**: row `greenhouse-data`, type **Dataset**, **Added by** you, one-person **Visibility**, a **green open** lock, an ID.
- [ ] Side panel: **Revision** (the first characters of the commit), samples and splits from `manifest.json`, the description (`DATASET.md` if the repository has one; this example has none, so "No DATASET.md in this repository"), and the **Git graph** with the commits. Read over git.
- [ ] **Credentials** table: your App, you, the **Last used** after use; projects appear after Step 7.
- [ ] After step 7: the task **greenhouse dataset read** in `examples` shows the repository, the commit, the content hash (the one in `data.dvc`) and the storage; the dataset row now lists `examples` in the credentials table, and its **Runs** tab lists that task.

## Database
- [ ] `repository`: key `github.com/<you>/greenhouse-data`, `roles` contains `dataset`, `owner` you, `state: "ok"`, `anonymous: false`.
- [ ] `repository_assignment`: (that repository, you, the App).
- [ ] `task.hyperparams.Datasets`: `<alias>/repo`, the commit and the hash for the reading task; `share` links the repository to `examples` with `inherited: true`.
- [ ] Dataset storage keys were issued for the push (server audit log `storage_keys`), never stored in a collection.

## FAIL signs
- `dataset add`/`check` is "invalid choice"; the push is refused with a footprint error; the lock is red although the App is installed on the repository.

## Result (2026-11-12, fresh stack)
PASS. Push of c31a20e (2500 samples, train 2000 / test 500) with the App (Contents and Workflows write). `doctor` first failed on auto-merge and branch protection, as documented; after enabling both: "No problems found". `check` passes. Task `greenhouse dataset read` has repo, commit, content hash `f82af0ad…​.dir`, storage `s3`. DB: repository (role dataset, state ok), assignment with App and `last_used`, share `projects`/`inherited`/`run_id` to `examples`. UI: row with green open lock, one-person Visibility, credentials table with project badge `examples`, Runs tab lists the task. Note: the dataset is published with `REPO=https://github.com/gianlucapargaetzi/greenhouse-data.git COMMIT=c31a20e50b572882d8d2a0f3e25df450edde22ab`.
