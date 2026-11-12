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

## Result (2026-11-12)
- PASS: the agent (`parg-nb`, kind agent, queue `parg-nb-f4cad6`) took the run from the command line; the clone made and enqueued in the web app ran the same commit `938f51a`; both completed; `repository_assignment.last_used` updated; the job installed the SDK and agent from wheels built from the checkouts (`cairnml @ file:///tmp/cairnml-0.0.5-...whl` in the task's Python packages).
- PASS step 5: deleting your credential row turns the lock red (`Access refused`); enqueueing a clone opens **Credentials not assigned** and stops; **Assign credentials** assigns and the enqueue continues by itself (README adjusted: no second enqueue).
- Found: the very first enqueue (empty GitHub repository) said "GitHub could not be reached"; now it says there is no commit.
- Note: the Enqueue dialog's queue field starts at `default`; choosing the agent's queue is part of the step (a task left in `default` stays Queued forever).
