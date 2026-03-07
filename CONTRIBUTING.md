# Contributing to agenti

Thank you for your interest in contributing to **agenti** — an AI-native repository that uses autonomous agent workflows to manage itself.

> ⚠️ **Important:** This is not a traditional code repository. It contains agent configurations and GitHub Actions workflows that drive autonomous AI behavior. Changes here have non-obvious consequences — please read this guide carefully before contributing.

## Table of Contents

- [What is agenti?](#what-is-agenti)
- [Repository structure](#repository-structure)
- [How to contribute](#how-to-contribute)
- [Modifying agent instructions](#modifying-agent-instructions)
- [Modifying workflow files](#modifying-workflow-files)
- [Pull request process](#pull-request-process)
- [Code of conduct](#code-of-conduct)

---

## What is agenti?

`agenti` is a self-managing repository powered by [GitHub Agentic Workflows (gh-aw)](https://github.com/github/gh-aw). The repository contains:

- **Agent definitions** (`.github/agents/*.md`): Instructions that guide AI agents
- **Workflow definitions** (`.github/workflows/*.md`): Scheduling and configuration for agentic runs
- **Compiled lock files** (`.github/workflows/*.lock.yml`): Generated output — do not edit directly

The agents autonomously review code, create issues, and implement improvements via pull requests.

---

## Repository structure

```
.github/
  agents/
    agenti-reviewer.md          # Agent that reviews the repo and files issues
    agentic-workflows.agent.md  # Dispatcher for gh-aw workflow tasks
    issue-implementer.agent.md  # Agent that implements open issues via PRs
  workflows/
    issue-implementer.md        # Workflow scheduling & config (source)
    issue-implementer.lock.yml  # Compiled lock file (generated — don't edit)
    copilot-setup-steps.yml     # Setup steps for Copilot agents
README.md
CONTRIBUTING.md                 # This file
```

---

## How to contribute

### Reporting bugs or suggesting improvements

1. [Open a GitHub issue](https://github.com/steffenkoenig/agenti/issues/new) with a clear description.
2. Use the issue title format: `[Category] Short description` (e.g., `[Agent Quality] Missing deduplication logic`).
3. Include the affected file(s) and a proposed solution if possible.

> Note: The `agenti-reviewer` agent may automatically file issues for quality improvements. Before filing a new issue, check for duplicates.

### Making changes

1. Fork the repository (or create a branch if you have write access).
2. Make your changes on a feature branch: `git checkout -b fix/issue-NN-short-description`
3. Commit with a conventional commit message: `fix:`, `feat:`, `docs:`, `chore:`, etc.
4. Push your branch and open a pull request against `main`.

---

## Modifying agent instructions

Agent instruction files (`.github/agents/*.md`) drive AI behavior. Changes here are **high-risk** because:

- A poorly-worded instruction can cause agents to create many low-quality issues or PRs
- Instructions affect live automated runs — there is no staging environment
- Changes take effect on the next scheduled workflow run

### Guidelines

- **Be specific**: Vague instructions lead to unpredictable agent behavior
- **Test your reasoning**: Read instructions from the perspective of an LLM — will it interpret them as you intend?
- **Constrain scope**: Always include limits (e.g., "create at most N issues per run")
- **Avoid prompt injection risk**: Never include untrusted user data in agent instructions
- **Keep instructions idempotent**: Agents run repeatedly — instructions should handle re-runs gracefully

---

## Modifying workflow files

Workflow source files (`.github/workflows/*.md`) are written in gh-aw markdown format and must be **compiled** before they take effect.

### Workflow edit + compile cycle

```bash
# Install gh-aw CLI (if not already installed)
gh extension install github/gh-aw

# Edit the source workflow
vim .github/workflows/issue-implementer.md

# Compile to lock file
gh aw compile issue-implementer

# Verify the compiled output
git diff .github/workflows/issue-implementer.lock.yml
```

> ⚠️ **Never edit `.lock.yml` files directly.** They are generated and will be overwritten on the next compile.

### Safe-output limits

Each workflow has safe-output limits in its frontmatter (e.g., `create-pull-request: max: 5`). These limits:

- Prevent runaway automation
- Are enforced by the gh-aw runtime — exceeding them causes silent rejection
- Must be consistent with the corresponding agent instructions

When changing an agent's action count, always update **both** the workflow `.md` source and the agent instructions.

---

## Pull request process

1. Ensure your branch is up-to-date with `main`
2. Keep PRs focused — one issue per PR
3. Reference the issue in the PR description: `Closes #NN`
4. The `agenti-reviewer` agent may automatically review your PR and leave comments
5. A maintainer will review and merge once all feedback is addressed

---

## Code of conduct

Please be respectful and constructive in all interactions. This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
