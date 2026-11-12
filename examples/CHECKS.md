# Checks for the examples

Each example has a `CHECKS.md` next to its README. It lists what must be true after the example, as **PASS** criteria you can look at: in the terminal, in the web app (UI) and in the database (DB). A box that cannot be ticked is a **FAIL**; write what you saw next to it.

Run the examples in order: each one builds on the state of the one before.

## Install from this checkout, not from PyPI

The newest SDK and agent are not on PyPI yet. Install both **editable from the checkouts** into the examples' virtual environment, instead of `pip install cairnml`:

```bash
source .venv/bin/activate
pip install -e /path/to/cairnml -e /path/to/cairnml-agent      # the checkouts of the branch that is being tested
pip install "cairnml[dataset]"                                  # the extras; the editable install already satisfies the package
pip show cairnml cairnml-agent | grep -E "^(Name|Version|Editable)"
```

PASS: `Editable project location` points at the checkouts, and `cairnml repository --help` lists `list, add, assign, unassign, check, delete, unshare, share, link, unlink`.

An editable (source-tree) install is also what makes **agent jobs use the same code**: the agent builds a wheel of the SDK and of itself from those source trees and installs them in every job container, never from PyPI. A copy installed into `site-packages` (a normal `pip install` of a wheel) makes the daemon fail with "is not a source tree of cairnml-agent". Check in the job's console that `/tmp/cairnml-0.0.5-py3-none-any.whl` and `/tmp/cairnml_agent-0.0.5-py3-none-any.whl` are installed (they are built from the checkouts), not downloaded.

## Looking at the database

```bash
docker exec cairnml-mongo mongosh --quiet backend --eval 'db.getCollectionNames()'
docker exec cairnml-mongo mongosh --quiet backend --eval 'db.repository.find({}, {key:1, roles:1, owner:1, state:1, anonymous:1, dismissed:1}).toArray()'
docker exec cairnml-mongo mongosh --quiet backend --eval 'db.repository_assignment.find().toArray()'
```

Enrolled machines (`device`) and the sign-in users are in the **`auth`** database: `docker exec cairnml-mongo mongosh --quiet auth --eval 'db.device.find().toArray()'`. The `backend` database holds the rest, including `user` (the profile of a user: `name`, `company`; the role comes from the identity provider, not from this collection).

The collections that matter here:

| Collection | Holds |
|---|---|
| `task` | runs: `name`, `status`, `project`, `user`, `type`, `hyperparams`, `script.repository`, `execution.queue`, `system_tags` |
| `project` | projects: `name`, `user` (owner), `members` |
| `repository` | one record per repository, dataset or registry: `key`, `roles`, `owner` (the creator), `state`, `anonymous`, `dismissed` |
| `repository_assignment` | how one user reads one repository: `repository`, `user`, `credential` or `none_needed`, `last_used` |
| `registry_entry` | the datasets a registry lists: `registry`, `name`, `source`, `link` |
| `share` | links: `resource_type: "repository"` with `scope: "projects"` (a project lists it; `inherited: true` when a run listed it, with `run_id`) or `scope: "public"` (shared by the admin) |
| `user_access` | credentials: `kind: "app"`, `app_id`, `label`, `scope` (`user` or `company`); the key is encrypted and never shown |
| `device` (database `auth`) | enrolled machines: `kind` (client or agent), `revoked` |

A secret must never be readable in any of them: PASS when no collection holds a PEM header (`BEGIN`), a token or a password in clear text.

## The words the UI uses

- **Access** lock: green open = CairnML can read it (a public repository needs no credential), red closed = it cannot.
- **Visibility**: one person = not shared, several people = shared by the admin.
- **Added by**: the user who listed it. **ID**: the first 8 characters of the record's id.
- A repository that a project lists cannot be deleted: its trash button is disabled and says why.
