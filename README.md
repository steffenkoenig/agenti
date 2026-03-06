# agenti

[![Agenti Reviewer](https://github.com/steffenkoenig/agenti/actions/workflows/agenti-reviewer.lock.yml/badge.svg)](https://github.com/steffenkoenig/agenti/actions/workflows/agenti-reviewer.lock.yml)
[![Issue Implementer](https://github.com/steffenkoenig/agenti/actions/workflows/issue-implementer.lock.yml/badge.svg)](https://github.com/steffenkoenig/agenti/actions/workflows/issue-implementer.lock.yml)

**agenti** is an AI-powered, self-evolving repository management system built on [GitHub Agentic Workflows (gh-aw)](https://github.com/github/gh-aw). It deploys a team of autonomous AI agents that continuously audit your codebase, open GitHub Issues for findings, implement those issues as pull requests, and even improve the agents themselves — all on a recurring schedule with no human intervention required.

At its core, agenti closes the loop between code review and code change: a reviewer agent scans the repository and files structured issues; an implementer agent picks those issues up and submits pull requests; and a workflow-management agent keeps all the underlying automation up to date. The result is a living repository that reflexively repairs and improves itself around the clock.

## Table of Contents

- [Architecture](#architecture)
- [Agents](#agents)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Workflows](#workflows)
- [Usage](#usage)
- [Contributing](#contributing)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   GitHub Repository                  │
│                                                      │
│  ┌──────────────────┐     ┌───────────────────────┐ │
│  │  Agenti Reviewer │────▶│   GitHub Issues        │ │
│  │  (every 2 hours) │     │   (findings & tasks)   │ │
│  └──────────────────┘     └──────────┬────────────┘ │
│                                       │              │
│  ┌──────────────────┐                 │              │
│  │ Issue Implementer│◀────────────────┘              │
│  │  (every 2 hours) │                                │
│  └────────┬─────────┘                                │
│           │  Pull Requests                           │
│           ▼                                          │
│  ┌──────────────────┐                                │
│  │  Main Branch     │                                │
│  └──────────────────┘                                │
│                                                      │
│  ┌────────────────────────────────────┐              │
│  │  Agentic Workflows Agent           │              │
│  │  (manages .github/workflows/*.md)  │              │
│  └────────────────────────────────────┘              │
└─────────────────────────────────────────────────────┘
```

Both scheduled agents run every two hours, are scoped to the `main` branch, and use a concurrency lock so only one instance of each agent runs at a time. All agent outputs go through a safe-outputs firewall that caps the number of issues, pull requests, and comments an agent can create per run, preventing runaway automation.

## Agents

### 1. Agenti Reviewer (`agenti-reviewer`)

A **Senior Architect / Repository Sentinel** that performs holistic, recursive audits of the entire repository. It reviews:

- **Code & Infrastructure** — logic efficiency, modernization opportunities, DRY/SOLID violations
- **Testing & Resilience** — coverage gaps, test quality, flaky tests
- **Documentation** — bus-factor risks, docs that are out of sync with code
- **Agents & Workflows (Recursive)** — reviews the other agents, proposes new specialist agents, and audits itself

For each finding the reviewer opens a structured GitHub Issue containing a current-state/desired-state description, impact rating (Critical / Warning / Enhancement), a step-by-step proposed solution, and a checklist of acceptance criteria.

**Safe-output limits per run:** max 10 issues · max 10 comments · max 1 noop

### 2. Issue Implementer (`issue-implementer`)

An **Autonomous Software Engineer** that fetches all open GitHub Issues, prioritizes them using explicit labels, community reactions, comments, and age, then implements up to 10 per run. For each selected issue it:

1. Produces a detailed task list (understanding, affected files, implementation steps, tests, docs, acceptance criteria)
2. Makes the required code changes
3. Adds or updates tests and documentation
4. Opens a pull request referencing the issue

**Safe-output limits per run:** max 5 pull requests · max 10 comments · max 1 noop

### 3. Agentic Workflows Agent (`agentic-workflows`)

A **Dispatcher / Workflow Engineer** that manages the gh-aw workflow definitions themselves. It routes requests to specialized sub-prompts for:

- Creating and updating workflow definitions (`.github/workflows/*.md`)
- Compiling `.md` sources to `.lock.yml` files via `gh aw compile`
- Debugging failed workflow runs
- Upgrading the gh-aw extension version across all workflows
- Generating reports and shared reusable workflow components

## Prerequisites

| Requirement | Version | Purpose |
|---|---|---|
| [GitHub CLI (`gh`)](https://cli.github.com/) | ≥ 2.x | Required by gh-aw extension |
| [gh-aw extension](https://github.com/github/gh-aw) | v0.53.6+ | Compiles and runs agentic workflows |
| GitHub Copilot | Business or Enterprise | Powers the AI agents |
| `COPILOT_GITHUB_TOKEN` secret | — | Repository secret used by workflows for API access |

## Setup

### 1. Fork or clone the repository

```bash
git clone https://github.com/steffenkoenig/agenti.git
cd agenti
```

### 2. Install the GitHub CLI and gh-aw extension

```bash
# Install GitHub CLI (see https://cli.github.com/ for platform-specific instructions)
gh auth login

# Install the gh-aw extension
gh extension install github/gh-aw
```

### 3. Configure repository secrets

In your repository settings, add the following secret:

| Secret | Description |
|---|---|
| `COPILOT_GITHUB_TOKEN` | A GitHub token with `repo` and `copilot` scopes |

### 4. Enable GitHub Actions

Ensure GitHub Actions is enabled for your repository. The compiled lock files (`.github/workflows/*.lock.yml`) are already checked in and will be picked up automatically by GitHub Actions.

### 5. (Optional) Edit agent prompts

The agent behaviour is defined in plain-English markdown files under `.github/agents/`. Edit these files to customise how the agents operate, then recompile the lock files:

```bash
gh aw compile .github/workflows/agenti-reviewer.md
gh aw compile .github/workflows/issue-implementer.md
```

## Workflows

| Workflow | Schedule | Trigger | Description |
|---|---|---|---|
| **Agenti Reviewer** | Every 2 hours | `schedule` / `workflow_dispatch` | Audits the repo and opens GitHub Issues |
| **Issue Implementer** | Every 2 hours | `schedule` / `workflow_dispatch` | Implements open issues and opens PRs |
| **Copilot Setup Steps** | On push / manual | `push` / `workflow_dispatch` | Provisions the gh-aw CLI environment |

Both primary workflows run only on the `main` branch and use a concurrency group to prevent parallel runs of the same workflow.

## Usage

### Trigger manually

```bash
# Run the reviewer agent once
gh workflow run agenti-reviewer.lock.yml

# Run the issue implementer once
gh workflow run issue-implementer.lock.yml
```

### Let it run automatically

Once the repository secrets are set and GitHub Actions is enabled, both workflows will trigger on their two-hour cron schedules automatically. No further action is required.

### Customise the agents

Open any file in `.github/agents/` in your editor. GitHub Copilot is enabled for markdown files in this repository, so you can use Copilot to help you refine agent instructions. After editing, recompile the affected workflow:

```bash
gh aw compile .github/workflows/<workflow-name>.md
```

Commit both the `.md` source and the regenerated `.lock.yml` file.

## Contributing

1. **Open an issue** — describe the bug, enhancement, or question. The Agenti Reviewer will periodically audit the repo and may open issues automatically too.
2. **Fork & branch** — create a feature branch from `main`.
3. **Make changes** — follow the existing code style; keep commits small and focused.
4. **Compile workflows** — if you edit any `.github/workflows/*.md` file, run `gh aw compile` and commit the resulting `.lock.yml`.
5. **Open a pull request** — reference the related issue in the PR description.

> **Note:** The Issue Implementer agent runs every two hours and may implement open issues automatically. If you are actively working on an issue, add a comment so the agent skips it.
