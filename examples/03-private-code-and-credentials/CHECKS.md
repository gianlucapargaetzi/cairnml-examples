# Checks: Example 3, private code and credentials

Needs your GitHub account and the GitHub App steps by hand (steps 3 and 4).

## GitHub (outside CairnML)
- [ ] `cairnml-private-demo` exists, is **private**, and a private browser window shows 404.
- [ ] The GitHub App exists and is installed on that repository only ("Only select repositories").
- [ ] The App's permissions are **Contents: Read and write** and **Workflows: Read and write**, everything else No access (read-only is enough for Example 4 alone, but Example 6 pushes).

## Terminal
- [ ] `cairnml credential list` shows the App with a working state.
- [ ] Before the assignment: `cairnml repository list` shows the repository with READ AS `not readable`; after it: `credential`.
- [ ] `cairnml repository add https://github.com/<you>/cairnml-private-demo --type code --project <id> --credential <id>` (if used instead of the UI) prints `credential`.

## UI
- [ ] **Settings → Access**: the App is listed, state OK. Adding it with a wrong key is refused with a reason, and nothing is saved.
- [ ] **Repositories & Datasets → Add repository or dataset**: type Code, the address, project examples. The new row has the type **Code**, **Added by** you, **Visibility** one person, an 8-character **ID**, and a **red closed** Access lock while nothing is assigned.
- [ ] Side panel → **Credentials**: one **empty** row (App "–", Owner you, Project `examples`, red lock) with only the lock button.
- [ ] Assign your credential: the Access lock turns **green open**; the Credentials table has one row (your App, you, `examples`, green lock, **Last used** filled after **Check now**).
- [ ] **Check now** reports the repository as readable. Assigning a credential that cannot read it is refused with the reason.
- [ ] The row's **trash is disabled** (the project `examples` lists it) and its tooltip says so. **More → Make shared** opens the share dialog (no company credential yet: it explains).
- [ ] **Project settings → Repositories** of `examples` lists it with the green lock and "Added by" you.

## Database
- [ ] `user_access`: one `kind: "app"` document, `scope: "user"`, `app_id`, `label`; the secret is encrypted (no `BEGIN` in clear text).
- [ ] `repository`: key `github.com/<you>/cairnml-private-demo`, `roles: ["code"]`, `owner` you, `state: "ok"`, `anonymous: false`.
- [ ] `repository_assignment`: one document (repository, you, `credential` = the App's id, `none_needed` false, `last_used` set after a check).
- [ ] `share`: one `scope: "projects"` link to `examples` (`inherited: false` when added by hand).

## FAIL signs
- The App's key can be read back anywhere; the lock is green without a credential for a private repository; the trash is enabled while a project lists the repository.
