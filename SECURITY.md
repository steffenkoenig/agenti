# Security Policy

## Supported Versions

This repository contains GitHub Agentic Workflow (gh-aw) configurations and agent instructions. The following components are actively maintained:

| Component | Maintained |
|---|---|
| `.github/workflows/*.md` (workflow sources) | ✅ Yes |
| `.github/workflows/*.lock.yml` (compiled) | ✅ Yes |
| `.github/agents/*.agent.md` | ✅ Yes |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub Issues.**

To report a security vulnerability, use [GitHub's private vulnerability reporting](https://github.com/steffenkoenig/agenti/security/advisories/new). You will receive an acknowledgement within **72 hours** and a resolution update within **7 days**.

Please include:

- A description of the vulnerability and its potential impact.
- The affected file(s) and line numbers where applicable.
- Steps to reproduce or a proof-of-concept.
- Any suggested remediation.

## Security Model

### Agent Workflow Firewall (AWF)

All agentic workflows execute inside the [Agent Workflow Firewall](https://github.github.com/gh-aw/reference/firewall/) sandbox. Outbound network traffic is restricted to an explicit domain allowlist. Review `GH_AW_INFO_ALLOWED_DOMAINS` in each `.lock.yml` file to understand the permitted domains for a given workflow.

### Principle of Least Privilege

Every workflow job requests only the GitHub token permissions it requires. The top-level `permissions:` block is set to `{}` (deny-all default) and individual jobs declare only the scopes they need. Review the `permissions:` blocks in each `.lock.yml` to verify.

### Action Pinning

All third-party GitHub Actions (`uses:`) are pinned to a full commit SHA to prevent supply-chain attacks via tag re-pointing. If you observe an action reference that uses a mutable tag or branch name, please report it.

### Safe Outputs

AI agents communicate with the GitHub API exclusively through the `safe-outputs` mechanism, which enforces per-run rate limits (e.g., at most 5 pull requests or 10 issues per workflow run). Agents cannot directly call GitHub write APIs.

### Prompt Injection

Agent instructions are reviewed by the [`security-auditor`](.github/agents/security-auditor.agent.md) specialist agent for prompt injection vulnerabilities, ensuring that user-supplied content (issue bodies, PR titles, comments) cannot hijack agent behaviour.

## Automated Security Auditing

A dedicated `Security Audit` workflow (`.github/workflows/security-audit.md`) runs automatically:

- On every pull request that modifies files under `.github/`.
- On a monthly schedule.
- On demand via `workflow_dispatch`.

The workflow uses the [`security-auditor`](.github/agents/security-auditor.agent.md) agent to check all six security domains:

1. Prompt Injection Detection
2. Permission Audit
3. Secret Hygiene
4. Action Pin Audit
5. Network Allowlist Review
6. Output Injection Audit

Findings are reported as GitHub Issues with severity labels.

## Known Security Considerations

### Action SHA Pinning

All `uses:` references in lock files are pinned to full commit SHAs by the `gh aw compile` toolchain. Never edit lock files manually — always recompile from the `.md` source.

### COPILOT_GITHUB_TOKEN Scope

The `COPILOT_GITHUB_TOKEN` secret used by agentic workflows should be scoped to the minimum permissions required. Periodically audit the token's organisation-level permissions via the GitHub token settings page.
