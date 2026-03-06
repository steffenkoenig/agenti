---
name: "Agenti Reviewer"
on:
  schedule: every 2 hours
concurrency:
  group: agenti-reviewer
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
permissions:
  contents: read
engine:
  id: copilot
  agent: agenti-reviewer
safe-outputs:
  create-issue:
    max: 10
  add-comment:
    max: 10
  noop:
    max: 1
---

Run the agenti-reviewer agent to perform a holistic audit of this repository and create GitHub Issues for any improvements found.
