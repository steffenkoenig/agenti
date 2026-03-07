---
name: "Stale Issue Janitor"
on:
  schedule: every 24 hours
  workflow_dispatch:
concurrency:
  group: stale-issue-janitor
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
permissions:
  contents: read
engine:
  id: copilot
  agent: stale-issue-janitor
safe-outputs:
  update-issue:
    max: 10
  add-comment:
    max: 10
  noop:
    max: 1
---

Run the stale-issue-janitor agent to scan all open issues and close any that have already been resolved by merged PRs or existing work in main.
