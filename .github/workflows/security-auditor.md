---
name: "Security Auditor"
on:
  schedule: every 7 days
concurrency:
  group: security-auditor
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
permissions:
  contents: read
engine:
  id: copilot
  agent: security-auditor
safe-outputs:
  create-issue:
    max: 5
  noop:
    max: 1
---

Run the security-auditor agent to perform a focused weekly security audit of this repository, covering workflow permissions, pinned action SHAs, secret scopes, prompt injection detection, and agent boundary verification.
