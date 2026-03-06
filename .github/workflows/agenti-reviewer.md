---
name: "Repository Sentinel"
on:
  schedule: every 168h
  workflow_dispatch:
concurrency:
  group: agenti-reviewer
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
permissions:
  contents: read
  issues: read
  pull-requests: read
engine:
  id: copilot
  agent: agenti-reviewer
safe-outputs:
  create-issue:
    max: 15
  add-comment:
    max: 5
  noop:
    max: 1
---

Run the agenti-reviewer agent to perform a holistic audit of this repository and create GitHub Issues for any improvements identified.
