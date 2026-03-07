# Contributing to agenti

Thank you for your interest in contributing to **agenti**! This guide explains how the repository is structured, how to safely make changes, and how to test those changes before opening a pull request.

## Table of Contents

- [How the Self-Improvement Loop Works](#how-the-self-improvement-loop-works)
- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Editing Agent Instructions](#editing-agent-instructions)
- [Editing and Compiling Workflows](#editing-and-compiling-workflows)
- [Testing Changes Locally](#testing-changes-locally)
- [Testing Workflow Changes via `workflow_dispatch`](#testing-workflow-changes-via-workflow_dispatch)
- [Branching and PR Conventions](#branching-and-pr-conventions)

---

## How the Self-Improvement Loop Works

agenti runs two scheduled agentic workflows that cooperate to keep the repository healthy and evolving:

1. **Agenti Reviewer** (runs every 2 hours) — Audits the repository holistically and opens GitHub Issues for any improvements it finds.
2. **Issue Implementer** (runs every 2 hours) — Picks up open GitHub Issues, implements them as code changes, and opens pull requests.

Both workflows are powered by GitHub Copilot. The agent behavior is defined in prompt files under `.github/agents/`, and the scheduling/permissions are defined in the workflow source files under `.github/workflows/*.md`. The compiled `.lock.yml` files are auto-generated and drive GitHub Actions.

> **Important:** Never edit `.lock.yml` files directly. Always edit the corresponding `.md` source file and recompile (see [Editing and Compiling Workflows](#editing-and-compiling-workflows)).

---

## Prerequisites

- A GitHub repository with **GitHub Copilot** enabled (Copilot Business or Copilot Enterprise plan required).
- The [`gh-aw`](https://github.github.com/gh-aw/introduction/overview/) CLI extension, if you want to edit or recompile workflow definitions:
  ```bash
  gh extension install github/gh-aw
  ```
- The `COPILOT_GITHUB_TOKEN` repository secret must be set. Workflows validate this secret at startup and fail immediately if it is missing.

---

## Repository Structure

```
.github/
  agents/
    agenti-reviewer.md              # Prompt/instructions for the Reviewer agent
    issue-implementer.agent.md      # Prompt/instructions for the Issue Implementer agent
    agentic-workflows.agent.md      # Shared gh-aw conventions used by all agents
  workflows/
    agenti-reviewer.md              # Workflow source (edit this, not the .lock.yml)
    agenti-reviewer.lock.yml        # Compiled workflow — DO NOT edit manually
    issue-implementer.md            # Workflow source (edit this, not the .lock.yml)
    issue-implementer.lock.yml      # Compiled workflow — DO NOT edit manually
    copilot-setup-steps.yml         # Environment setup for the Copilot Agent runner
  copilot-instructions.md           # PR Architect agent instructions (review and advisory only)
CONTRIBUTING.md                     # This file
README.md                           # Project overview and setup instructions
```

---

## Editing Agent Instructions

Agent instruction files live in `.github/agents/`. Each file is a Markdown document that serves as the system prompt for that agent.

**To change agent behavior:**

1. Open the relevant agent file:
   - **Reviewer logic** → `.github/agents/agenti-reviewer.md`
   - **Implementer logic** → `.github/agents/issue-implementer.agent.md`
   - **Shared gh-aw conventions** → `.github/agents/agentic-workflows.agent.md`

2. Edit the instructions carefully. Keep prompts unambiguous and atomic — each skill or constraint should have a single, clear purpose to minimize hallucination risk.

3. Commit the changed agent file(s) **together** with any related workflow changes.

> **Note:** Changes to agent instructions take effect on the next scheduled workflow run (or immediately via `workflow_dispatch`). No recompilation step is needed for agent files — only workflow `.md` files require a recompile step.

---

## Editing and Compiling Workflows

Workflow definitions live in `.github/workflows/*.md`. These source files control the schedule, permissions, engine configuration, and safe-output limits for each workflow. The corresponding `.lock.yml` files are auto-generated from them and must never be edited by hand.

**To modify a workflow (e.g., change the schedule):**

1. Edit the relevant `.md` source file:
   - **Reviewer schedule/config** → `.github/workflows/agenti-reviewer.md`
   - **Implementer schedule/config** → `.github/workflows/issue-implementer.md`

2. Recompile the workflow to regenerate the `.lock.yml`:
   ```bash
   gh aw compile
   ```

3. Commit **both** the `.md` source file and the regenerated `.lock.yml` file together. Never commit one without the other.

**Common customizations in the frontmatter:**

| Field | Description | Example |
|---|---|---|
| `schedule` | How often the workflow runs | `every 2 hours` |
| `safe-outputs.<key>.max` | Maximum number of times an agent may call that output action per run | `max: 5` |
| `permissions` | GitHub token permissions granted to the workflow | `contents: read` |

> **Note:** `gh aw` schedule only supports `every N minutes/hours/days` format. Weekly or monthly cadences are not valid — use `every 30 days` as the closest approximation.

> **Note:** In `gh aw` strict mode, keep the top-level `permissions` in the `.md` source as minimal as possible (typically read-only, e.g. `contents: read`). When you need to create or update issues, use `safe-outputs` (for example `safe-outputs.create-issue`); `gh aw` will generate helper jobs in the compiled `.lock.yml` with the necessary elevated permissions such as `issues: write` for those actions.

---

## Testing Changes Locally

Because the workflows run inside GitHub Actions with Copilot, there is no fully local execution environment. However, you can validate several aspects of your changes before pushing:

1. **YAML lint** — Run YAML linting on the compiled `.lock.yml` files:
   ```bash
   yamllint .github/workflows/
   ```

2. **Agent/workflow validation** — Use `gh aw compile` to validate your changes. If compilation succeeds without errors, the workflow definition is syntactically valid:
   ```bash
   gh aw compile
   ```

3. **Dry-run review of agent prompts** — Read through the agent instruction file and verify that instructions are clear, unambiguous, and do not conflict. Pay particular attention to the `safe-outputs` keys the agent is allowed to call.

4. **`gh aw compile` output** — Inspect the regenerated `.lock.yml` to confirm the schedule, permissions, and safe-output limits look correct after compilation.

---

## Testing Workflow Changes via `workflow_dispatch`

The safest way to validate changes to workflow logic or agent instructions without waiting for the scheduled run is to trigger the workflow manually:

```bash
# Trigger the Agenti Reviewer
gh workflow run "Agenti Reviewer"

# Trigger the Issue Implementer
gh workflow run "Issue Implementer"
```

Or use the GitHub Actions UI: **Actions → select the workflow → Run workflow**.

After triggering, monitor the run:

```bash
gh run list --workflow "Agenti Reviewer"
gh run watch   # follow the most recent run in real time
```

Check the run logs to confirm the agent behaved as expected before merging your changes.

---

## Branching and PR Conventions

- **Branch from `main`** for all changes: `git checkout -b your-feature-branch`.
- **Commit related changes together** — always commit the `.md` source file and its compiled `.lock.yml` as a single commit when modifying workflows.
- **Open a pull request** against `main`. Provide a clear description of what changed and why.
- **Avoid editing `.lock.yml` files directly.** If a PR contains manual edits to a `.lock.yml`, it will be flagged for review.
- The **Issue Implementer** agent may open PRs automatically. These follow the same conventions and should be reviewed like any other PR before merging.
- If the self-improvement loop opens an issue you disagree with, close it with a comment explaining the reasoning so the agent can learn from the context.
