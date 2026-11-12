# Checks for the examples

Each example has a `CHECKS.md` next to its README. It lists what must be true after the example, as **PASS** criteria you can look at: in the terminal, in the web app (UI) and in the database (DB). A box that cannot be ticked is a **FAIL**; write what you saw next to it.

Run the examples in order: each one builds on the state of the one before.

## Install from this checkout, not from PyPI

The newest SDK and agent are not on PyPI yet. Before Example 0, step 6, install both from the local checkouts into the examples' virtual environment, instead of `pip install cairnml`:

```bash
source .venv/bin/activate
pip install -e /path/to/cairnml /path/to/cairnml-agent     # the checkouts of the branch that is being tested
pip show cairnml cairnml-agent | grep -E "^(Name|Version|Editable)"
```

PASS: `Editable project location` points at the checkouts, and `cairnml repository --help` lists `list, add, assign, unassign, check, delete, unshare, share, link, unlink`.

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

## Jobs on an agent must use the same SDK and agent

A job runs in a container, and the container installs the SDK and the agent itself. To test an unreleased state, the agent installs them from a local package index instead of PyPI:

```bash
cd cairnml-server && scripts/build-dev-wheels.sh                 # wheels 0.0.5+dev.<commit> of ../cairnml and ../cairnml-agent
# put the wheels in <dir>/simple/<package>/ with an index.html each, then:
python3 -m http.server 8099 --directory <dir>
# ~/.cairnml/agent/cairnml-agent.conf:
agent.package_manager.extra_index_url: ["http://localhost:8099/simple"]
```

A local version sorts above the release, so `pip install cairnml` in the job takes it. The agent refuses `-v` mounts in `extra_docker_arguments` on purpose, so a mount of the checkouts does not work. PASS: the job's console shows `cairnml-0.0.5+dev.<commit>` being installed.

## The words the UI uses

- **Access** lock: green open = CairnML can read it (a public repository needs no credential), red closed = it cannot.
- **Visibility**: one person = not shared, several people = shared by the admin.
- **Added by**: the user who listed it. **ID**: the first 8 characters of the record's id.
- A repository that a project lists cannot be deleted: its trash button is disabled and says why.
