---
name: "Repository Sentinel"
on:
  schedule: every week
  workflow_dispatch:
concurrency:
  group: agenti-reviewer
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
permissions:
  contents: read
  issues: write
  pull-requests: read
engine:
  id: copilot
  agent: agenti-reviewer
safe-outputs:
  create_issue:
    max: 15
  add_comment:
    max: 5
  noop:
    max: 1
---

Run the agenti-reviewer agent to perform a holistic audit of this repository and create GitHub Issues for any improvements identified.
