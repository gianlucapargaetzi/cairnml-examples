# Checks: Example 4, run on an agent

The agent runs on **this machine**, installed from the local checkout (see `../CHECKS.md`).

## Terminal
- [ ] `cairnml-agent` is the editable local checkout; enrolment as an agent succeeds; `cairnml-agent daemon` stays running and prints that it serves its own queue.
- [ ] `python train.py --epochs 3 --queue <queue>` queues the run and ends; the daemon logs that it took the job, cloned the repository and ran it.
- [ ] The daemon needed **no Git credential of its own** (no prompt, no token in its config).

## UI
- [ ] **Agents & Queues**: this machine is listed; a queue named after the machine plus a suffix exists. The job waits there, then runs on this machine with progress.
- [ ] Project **examples**: the task goes **Queued → Running → Completed**; **Execution → Source code** shows the private repository, the recorded commit and a **green open** lock.
- [ ] **Repositories & Datasets**: the credentials row of `cairnml-private-demo` shows **Last used** updated by the job's token.
- [ ] Clone the task (Draft) and **Enqueue** it in the web app: it runs the same commit.
- [ ] Step 5: delete **your** credential row; the Access lock turns red closed; enqueueing a clone opens **Credentials not assigned** with **Assign credentials**; after assigning, enqueue runs. A task of a repository nobody can read becomes **Failed** (not Aborted) with the reason.
- [ ] `--image python:3.12-slim` runs the job in that image.

## Database
- [ ] `device`: a second document, kind agent, not revoked; `queue`: one for this machine.
- [ ] `task`: `execution.queue` = that queue, `script.repository` = the private repository, `script.version_num` = the pushed commit, `status` completed.
- [ ] `repository_assignment.last_used` is newer than before the run. After step 5 the document is gone while step 5 lasts, then back.
- [ ] `repository`: still one record for the private repository (the second project or run did not duplicate it).

## FAIL signs
- The job fails to clone although a credential is assigned; the job runs with the credential of somebody else; a token or key appears in the daemon log.
