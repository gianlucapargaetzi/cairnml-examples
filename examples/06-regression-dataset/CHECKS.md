# Checks: Example 6, a dataset of your own

Needs the GitHub App installed on the **new** repository `greenhouse-data` (step 4, by hand).

## Terminal
- [ ] Before the push: the App has Contents and Workflows **write** and the installation accepted them. With a read-only App the push is refused with the reason (FAIL of the example, not of CairnML: fix the App and repeat).
- [ ] `cairnml dataset --help` lists `init, remote, clone, status, add, check, commit, doctor, push, get, create, list, cache`.
- [ ] `cairnml dataset remote add <url> --credential <id>` sets origin and the storage, lists the dataset and does **not** warn about reachability.
- [ ] `cairnml dataset add`, `commit` and `push` succeed; `cairnml dataset doctor` reports nothing missing; `cairnml dataset check` passes.
- [ ] `cairnml dataset list` and `cairnml repository list --type dataset` show `greenhouse-data`, READ AS `credential`.
- [ ] `REPO` and `COMMIT` are noted for Examples 7 to 11.

## UI
- [ ] **Repositories & Datasets**: row `greenhouse-data`, type **Dataset**, **Added by** you, one-person **Visibility**, a **green open** lock, an ID.
- [ ] Side panel: **Revision** (the first characters of the commit), samples and splits from `manifest.json`, the description (`DATASET.md`), and the **Git graph** with the commits. Read over git.
- [ ] **Credentials** table: your App, you, the **Last used** after use; projects appear after Step 7.
- [ ] After step 7: the task **greenhouse dataset read** in `examples` shows the repository, the commit, the content hash (the one in `data.dvc`) and the storage; the dataset row now lists `examples` in the credentials table, and its **Runs** tab lists that task.

## Database
- [ ] `repository`: key `github.com/<you>/greenhouse-data`, `roles` contains `dataset`, `owner` you, `state: "ok"`, `anonymous: false`.
- [ ] `repository_assignment`: (that repository, you, the App).
- [ ] `task.hyperparams.Datasets`: `<alias>/repo`, the commit and the hash for the reading task; `share` links the repository to `examples` with `inherited: true`.
- [ ] Dataset storage keys were issued for the push (server audit log `storage_keys`), never stored in a collection.

## FAIL signs
- `dataset add`/`check` is "invalid choice"; the push is refused with a footprint error; the lock is red although the App is installed on the repository.
