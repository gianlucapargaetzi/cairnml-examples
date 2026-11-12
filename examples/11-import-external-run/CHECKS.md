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
