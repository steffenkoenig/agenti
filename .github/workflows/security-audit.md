---
name: "Security Audit"
on:
  pull_request:
    paths:
      - ".github/**"
  schedule: every 30 days
  workflow_dispatch:
concurrency:
  group: security-audit
  cancel-in-progress: false
if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch' || github.event_name == 'pull_request'
permissions:
  contents: read
engine:
  id: copilot
  agent: security-auditor
safe-outputs:
  create-issue:
    max: 10
  noop:
    max: 1
---

Run the security-auditor agent to perform a full security review of this repository's agentic workflow files, agent instructions, workflow permissions, action pins, network allowlist, and safe-output configurations. Report every finding as a GitHub Issue.
