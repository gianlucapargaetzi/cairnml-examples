# Checks: Example 5, CIFAR-10 through the dataset registry

## Terminal
- [ ] `python train.py` runs with the default registry `cairnml-dataset-registry` (public) and needs nothing set up; it ends with accuracy close to Example 2.
- [ ] `cairnml repository list --type registry` shows the registry, READ AS `public`.

## UI
- [ ] **Repositories & Datasets**: a row `cairnml-dataset-registry`, type **Registry**, **Added by** the user of the run (or the project's owner), a **green open** Access lock; its ID is shown.
- [ ] A click on the row opens its datasets (`cifar10`, `coco-fashion`, `fashion-mnist`, and the others the registry lists); each shows its metadata (samples, splits) in the panel.
- [ ] The **Credentials** table has **one empty row** with the project `examples` and a green open lock (a public registry needs no credential).
- [ ] The **Runs** tab (data table) lists the run of this example (status, "Registry", user, created).
- [ ] The row's refresh button re-reads the registry and reports the counts; the trash is disabled (the project lists it).
- [ ] The task's **Configuration** lists the dataset `cifar10`, its revision, the adapter and the registry commit; the validation accuracy is close to Example 2's.
- [ ] A **private** registry added beforehand shows the red lock until a credential is assigned; reading it then works.

## Database
- [ ] `repository`: key `github.com/gianlucapargaetzi/cairnml-dataset-registry`, `roles: ["registry"]`, `anonymous: true`, `state: "ok"`, `read_at` set.
- [ ] `registry_entry`: one document for every dataset the registry lists, `registry` = the repository's id, `source` and `link` set. Read over **git** (the server log has no GitHub REST call for it).
- [ ] `share`: a `scope: "projects"` link to `examples` with `inherited: true` and `run_id` = this task.
- [ ] `task.hyperparams.Datasets` holds `cifar10/external_repo` pointing at the registry.
- [ ] No `repository_assignment` is needed.

## FAIL signs
- The registry has no entries; a GitHub rate-limit error appears; the registry is only listed after the task ends (it must be listed when the parameters are recorded).
