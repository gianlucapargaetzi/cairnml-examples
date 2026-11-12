# Checks: Example 10, the life of a task

## Terminal
- [ ] Each step of the script prints what it did; the destructive ones need `--yes`; the last step prints the status of the base task and says the clone is "not created".

## UI (look after each step)
- [ ] 2. **lifecycle base**: Completed, `lr` and `hidden` in Configuration.
- [ ] 3. **lifecycle clone**: **Draft**, changed learning rate, not running.
- [ ] 4. Queue the clone: **Queued** in the queue, then (with the agent, as in Example 4) runs and Completes; the web app **Enqueue** gives the same.
- [ ] 5. **Reset**: back to Draft.
- [ ] 6. **Archive**: disappears from the task list, visible under **Open archive**; un-archive brings it back.
- [ ] 7. **Move** to another project: it shows there and no longer in `examples`.
- [ ] 8. **Publish** the base task: status **Published**, no longer editable.
- [ ] 9. **Delete** the clone: gone from both the list and the archive.

## Database
- [ ] `task`: base `status: "published"`; the clone absent after step 9; after step 6 the clone had `system_tags` containing `archived`; after step 7 `project` is the other project's id.
- [ ] `project`: the second project exists (created by the move).

## FAIL signs
- Enqueue of a Draft leaves it Draft; delete leaves a document; publish succeeds on a task that is still running.

## Result (2026-11-12)
- PASS after one fix, step by step in the database: base completed (`system_tags: development`); clone `created` (Draft) in `examples`; enqueue → `queued` on `default`; dequeue/reset → `created`; archive → `system_tags: archived`, unarchive removes it; move → the clone's `project` is `examples scratch` (project created); publish → base `published`; delete → the clone is gone; status prints "clone: not created yet".
- Found and fixed: `Task.clone(..., project="examples")` is refused by the server ("Invalid project id: id=examples") because the project must be an ID; the script now passes the base task's project ID.
