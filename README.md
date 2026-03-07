# agenti

[![Agenti Reviewer](https://github.com/steffenkoenig/agenti/actions/workflows/agenti-reviewer.lock.yml/badge.svg)](https://github.com/steffenkoenig/agenti/actions/workflows/agenti-reviewer.lock.yml)
[![Issue Implementer](https://github.com/steffenkoenig/agenti/actions/workflows/issue-implementer.lock.yml/badge.svg)](https://github.com/steffenkoenig/agenti/actions/workflows/issue-implementer.lock.yml)
[![Stale Issue Janitor](https://github.com/steffenkoenig/agenti/actions/workflows/stale-issue-janitor.lock.yml/badge.svg)](https://github.com/steffenkoenig/agenti/actions/workflows/stale-issue-janitor.lock.yml)

**agenti** is an AI-powered, self-evolving repository management system built on [GitHub Agentic Workflows (gh-aw)](https://github.com/github/gh-aw). It deploys a team of autonomous AI agents that continuously audit your codebase, open GitHub Issues for findings, implement those issues as pull requests, and even improve the agents themselves — all on a recurring schedule with no human intervention required.

Three agentic workflows run on a schedule and keep the repository healthy:

| Workflow | Trigger | What it does |
|---|---|---|
| **Agenti Reviewer** | Every 2 hours (configurable) | Audits the repository holistically and opens GitHub Issues for any improvements it finds |
| **Issue Implementer** | Every 2 hours (configurable) | Picks up open GitHub Issues, implements the changes, and opens pull requests |
| **Security Auditor** | Weekly (configurable) | Performs a dedicated security audit covering workflow permissions, pinned action SHAs, secret scopes, prompt injection detection, and agent boundary verification |
| **Stale Issue Janitor** | Daily (configurable) | Scans open issues and closes any that have been resolved by merged PRs or existing work in `main` |

At its core, agenti closes the loop between code review and code change: a reviewer agent scans the repository and files structured issues; an implementer agent picks those issues up and submits pull requests; and a workflow-management agent keeps all the underlying automation up to date. The result is a living repository that reflexively repairs and improves itself around the clock.

## Table of Contents

- [Architecture](#architecture)
- [Agents](#agents)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Workflows](#workflows)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

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

```
.github/
  agents/
    agenti-reviewer.md                # Agent instructions for the reviewer
    issue-implementer.agent.md        # Agent instructions for the implementer
    security-auditor.agent.md         # Agent instructions for the security auditor
    stale-issue-janitor.agent.md      # Agent instructions for the stale issue janitor
    agentic-workflows.agent.md        # Shared gh-aw workflow conventions
  workflows/
    agenti-reviewer.md                # Workflow definition (source)
    agenti-reviewer.lock.yml          # Compiled workflow (do not edit manually)
    issue-implementer.md              # Workflow definition (source)
    issue-implementer.lock.yml        # Compiled workflow (do not edit manually)
    security-auditor.md               # Workflow definition (source)
    security-auditor.lock.yml         # Compiled workflow (do not edit manually)
    stale-issue-janitor.md            # Workflow definition (source)
    stale-issue-janitor.lock.yml      # Compiled workflow (do not edit manually)
    copilot-setup-steps.yml           # Environment setup for Copilot Agent
```
**Safe-output limits per run:** max 10 issues · max 10 comments · max 1 noop

### 2. Issue Implementer (`issue-implementer`)

An **Autonomous Software Engineer** that fetches all open GitHub Issues, prioritizes them using explicit labels, community reactions, comments, and age, then implements up to 5 issues per run (subject to safe-output limits). For each run it:

1. Produces a detailed task list for the selected issues (understanding, affected files, implementation steps, tests, docs, acceptance criteria)
2. Makes the required code changes
3. Adds or updates tests and documentation
4. Opens one or more pull requests referencing the implemented issues (possibly grouping several issues per pull request to honor safe-output limits)

**Safe-output limits per run:** max 5 pull requests · max 10 comments · max 1 noop

### 3. Stale Issue Janitor (`stale-issue-janitor`)

A **Janitorial Agent** that runs daily and keeps the issue backlog clean. It scans all open issues and closes any that have been resolved — either because a merged pull request references them (via `Closes #N`, `Fixes #N`, or `Resolves #N`) or because the work they requested is demonstrably present in the `main` branch. Before closing an issue the agent posts an explanatory comment citing the reason. Issues that are old but not clearly resolved are labeled `stale` for human review.

Guard rails prevent runaway closures:
- Only closes issues that are **at least 7 days old**
- Never closes issues that have an **open pull request** actively implementing them
- Never closes issues labeled `in-progress`, `do-not-close`, or `pinned`
- Caps at **10 close operations per run**

**Safe-output limits per run:** max 10 issue updates · max 10 comments · max 1 noop

### 4. Agentic Workflows Agent (`agentic-workflows`)

A **Dispatcher / Workflow Engineer** helper agent intended for manual, on-demand use (there is no scheduled workflow that runs it automatically). It routes requests to specialized sub-prompts for:

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
# Edit .github/workflows/agenti-reviewer.md, issue-implementer.md, or security-auditor.md, then:
gh aw compile
```

### 3. Configure repository secrets

In your repository settings, add the following secret:

| Secret | Description |
|---|---|
| `COPILOT_GITHUB_TOKEN` | A GitHub token with `repo` and `copilot` scopes |

### 4. Enable GitHub Actions

Ensure GitHub Actions is enabled for your repository. The compiled lock files (`.github/workflows/*.lock.yml`) are already checked in and will be picked up automatically by GitHub Actions.

### 5. (Optional) Edit agent prompts

Agent behavior is defined in plain-English markdown files under `.github/agents/`. Edit these files to customize how the agents operate, then commit your changes. No recompilation is needed for agent prompt-only edits — recompilation is only required when you change a workflow definition file (`.github/workflows/*.md`).

## Workflows

| Workflow | Schedule | Trigger | Description |
|---|---|---|---|
| **Agenti Reviewer** | Every 2 hours | `schedule` / `workflow_dispatch` | Audits the repo and opens GitHub Issues |
| **Issue Implementer** | Every 2 hours | `schedule` / `workflow_dispatch` | Implements open issues and opens PRs |
| **Stale Issue Janitor** | Daily | `schedule` / `workflow_dispatch` | Closes resolved issues and labels stale ones |
| **Copilot Setup Steps** | On push / manual | `push` / `workflow_dispatch` | Provisions the gh-aw CLI environment |

Both primary workflows run only on the `main` branch and use a concurrency group to prevent parallel runs of the same workflow.

## Usage

### Trigger manually

```bash
gh workflow run "Agenti Reviewer"
gh workflow run "Issue Implementer"
gh workflow run "Security Auditor"
gh workflow run "Stale Issue Janitor"
```

### Let it run automatically

```bash
gh run list --workflow "Agenti Reviewer"
gh run list --workflow "Issue Implementer"
gh run list --workflow "Security Auditor"
gh run list --workflow "Stale Issue Janitor"
```
Once the repository secrets are set and GitHub Actions is enabled, all scheduled workflows will trigger automatically. No further action is required.

### Customize the agents

Open any file in `.github/agents/` in your editor. GitHub Copilot is enabled for markdown files in this repository, so you can use Copilot to help you refine agent instructions.

After editing an agent file, simply commit your changes. Recompilation is only required if you also modify a workflow definition in `.github/workflows/*.md` (see the [Contributing](#contributing) section).

## Contributing

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on editing agent instructions, compiling workflows, testing changes, and PR conventions.

## License

This project is licensed under the [MIT License](LICENSE).
> **Note:** The Issue Implementer agent runs every two hours and may implement open issues automatically.
