# Checks: Example 11, import an outside run

## Terminal
- [ ] The legacy script runs and exports its files; `cairnml import prepare ...` writes the ZIP and prints a summary; no error about missing columns.

## UI
- [ ] **Import** in the web app takes the ZIP and creates a task: **Completed**, with the legacy scalars as curves, the parameters under **Configuration** and the files as artifacts; the legacy names are mapped to the CairnML names (see the table in the README).
- [ ] Importing the **same ZIP twice** gives **two** tasks.
- [ ] The imported task has no source repository (it never ran under CairnML): **Execution → Source code** is empty and **Repositories & Datasets** gains **no** record.

## Database
- [ ] `task`: one new document per import, `status` completed, `script.repository` empty; scalar events exist for it.
- [ ] `repository`: unchanged.

## FAIL signs
- The import "succeeds" with 0 scalars; the second import overwrites the first; a repository record appears.

## Result (2026-11-12, fresh stack)
PASS (after a deployment fix). The legacy script ran (best validation loss 0.3328, R2 0.9787); `export_to_cairnml.py` wrote the ZIP through `cairnml import prepare`. **Import run** (project folders page, `projects/<id>/folders`) created a Completed task with 90 scalar values and 2 files, no source repository, and no `repository` record; importing the same ZIP again gave a second task.
Found by running it: the browser sends the ZIP straight to the object store through a presigned URL, and the store sent no CORS headers, so the upload failed ("the store could not be reached"). The deployment now sets `RUSTFS_CORS_ALLOWED_ORIGINS` (default `*`; the signature in the URL is the authorisation, `CAIRNML_STORAGE_CORS_ORIGINS` narrows it).
