# Security Policy

## Supported Versions

The following versions of **agenti** are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

Only the latest code on the `main` branch is actively maintained. No legacy version branches are currently supported.

---

## Reporting a Vulnerability

We take security vulnerabilities seriously, especially given that **agenti** is an autonomous agent with access to a `COPILOT_GITHUB_TOKEN` for GitHub Copilot inference and separate GitHub API credentials (such as `GITHUB_TOKEN` or the MCP server token) that allow it to create pull requests, comment on issues, and interact with the GitHub API on a scheduled basis.

### How to Report

**Please do NOT open a public GitHub Issue for security vulnerabilities.**

Instead, use **[GitHub Private Vulnerability Reporting](../../security/advisories/new)** to disclose vulnerabilities privately:

1. Navigate to the **Security → Advisories** tab of this repository and click **"Report a vulnerability"**.
2. Fill in the details described in the [What to Include](#what-to-include-in-a-report) section below.

If you are unable to use GitHub's private reporting, you may contact the repository owner directly via GitHub ([@steffenkoenig](https://github.com/steffenkoenig)).

---

## Expected Response Timeline

| Action                              | Target Timeframe |
| ----------------------------------- | ---------------- |
| Acknowledgement of report           | Within 3 days    |
| Initial triage and severity rating  | Within 7 days    |
| Fix or mitigation plan communicated | Within 14 days   |
| Patch released (for valid issues)   | Within 30 days   |

We will keep you informed throughout the process. If you have not received a response within the expected timeframe, please follow up.

---

## What to Include in a Report

To help us triage and reproduce the vulnerability quickly, please include:

- **Description**: A clear summary of the vulnerability and its potential impact.
- **Affected component**: Which file(s), workflow(s), or agent(s) are involved (e.g., `issue-implementer.agent.md`, `agenti-reviewer.agent.md`).
- **Steps to reproduce**: A minimal, reproducible sequence of steps or a proof-of-concept.
- **Impact**: What an attacker could achieve by exploiting this issue (e.g., token exfiltration, unauthorized code commits, prompt injection).
- **Suggested fix** (optional): If you have a proposed mitigation or patch.

---

## AI Agent-Specific Security Concerns

**agenti** uses Large Language Model (LLM)-based agents to autonomously process GitHub issues and create pull requests. This introduces attack vectors that are specific to AI-powered systems.

### Prompt Injection

Prompt injection occurs when untrusted input (e.g., issue titles, issue bodies, PR descriptions, or code comments) manipulates the agent's instructions in unintended ways.

**Risk**: A malicious actor could craft a GitHub Issue with content designed to override agent instructions — for example, instructing the agent to exfiltrate secrets, modify unrelated files, or bypass safety constraints.

**Mitigations in place**:
- Agent instructions are defined in structured `.agent.md` files with explicit safe-output constraints.
- The `safe-outputs` system limits permitted actions (e.g., `create_pull_request` max 5, `noop` max 1).
- Agents do not have direct `git push` access; all changes go through reviewed pull requests.

**Please report** any issue or pull request content that you believe could be used as a prompt injection payload.

### Token Permission Model

The `COPILOT_GITHUB_TOKEN` secret used in agentic workflows grants the agent access to the GitHub API. Key facts about this token:

- It is scoped to repository-level operations (issues, pull requests, code).
- It does **not** have organization-level admin permissions.
- The token is never logged or surfaced in workflow outputs.
- All agent actions are limited by the `safe-outputs` mechanism defined in each workflow.

If you believe the token is over-privileged or has been exposed, please report it immediately using the private disclosure process above.

---

## Out of Scope

The following are **not** considered security vulnerabilities for this project:

- Issues that require the attacker to already have write access to the repository.
- Theoretical vulnerabilities with no realistic exploit path.
- Rate limiting or denial-of-service on the GitHub API (report these to GitHub directly).
- Bugs in GitHub Actions itself (report these to GitHub).
- Issues in third-party actions or dependencies that are not modified by this repository.

---

## Disclosure Policy

We follow a **coordinated disclosure** model:

1. Reporter submits a private report.
2. We triage, confirm, and develop a fix.
3. Once a fix is released, we will credit the reporter in the security advisory (unless they prefer to remain anonymous).
4. Public disclosure happens after the fix is available.

Thank you for helping keep **agenti** and its users safe.
