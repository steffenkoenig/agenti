---
name: "Issue Implementer"
on:
  schedule: every 4 hours
  workflow_dispatch:
concurrency:
  group: issue-implementer
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
permissions:
  contents: read
  issues: read
  pull-requests: read
engine:
  id: copilot
  agent: issue-implementer
safe-outputs:
  create-pull-request:
    max: 10
  noop:
    max: 1
---

Run the issue implementer agent to implement open issues in this repository.
