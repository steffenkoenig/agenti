# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

To report a security vulnerability, please use [GitHub's private vulnerability reporting](https://github.com/steffenkoenig/agenti/security/advisories/new).

Alternatively, you can email the repository owner directly. You can find contact information in the [GitHub profile](https://github.com/steffenkoenig).

### What to include

When reporting a vulnerability, please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce the issue
- Any relevant logs, screenshots, or proof-of-concept code
- Your suggested fix (if any)

### Response timeline

- **Acknowledgement**: Within 3 calendar days of receiving your report
- **Initial triage**: Within 7 calendar days
- **Resolution**: Depends on severity; critical issues are prioritized

## Security Considerations for This Repository

This repository contains autonomous AI agent configurations that:

- **Create pull requests** automatically on a schedule
- **Read repository contents** and GitHub issue data
- **Execute agent workflows** via GitHub Actions

### Threat model

Key security concerns for this repo include:

- **Prompt injection**: Malicious content in issues/PRs could influence agent behavior. All issue and PR bodies are treated as untrusted data.
- **Token permissions**: Agents use the minimum required GitHub token permissions (see workflow frontmatter `permissions:` blocks).
- **Safe-output limits**: Workflow configurations cap the number of GitHub API actions per run to prevent runaway automation.
- **Secrets exposure**: No secrets should ever be committed to agent instruction files or workflow definitions.

### Responsible disclosure

We are committed to working with security researchers to investigate and address reported vulnerabilities. We request that you:

1. Give us reasonable time to investigate and mitigate the issue before any public disclosure.
2. Avoid accessing or modifying data that does not belong to you.
3. Act in good faith and avoid disrupting the repository's normal operations.

We will not take legal action against researchers who responsibly disclose vulnerabilities following these guidelines.
