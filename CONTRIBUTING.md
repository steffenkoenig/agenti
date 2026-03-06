# Contributing to agenti

Thank you for your interest in contributing! This guide explains how to set up your development environment, understand the repository architecture, and submit changes safely.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Understanding the Architecture](#understanding-the-architecture)
3. [Making Changes to Agent Instructions](#making-changes-to-agent-instructions)
4. [Compiling Workflows](#compiling-workflows)
5. [Testing Changes](#testing-changes)
6. [PR Process](#pr-process)
7. [AI-Specific Guidelines](#ai-specific-guidelines)

---

## Development Setup

### Prerequisites

- [GitHub CLI (`gh`)](https://cli.github.com/) — version 2.x or later
- The [`gh-aw` extension](https://github.com/github/gh-aw) — GitHub Agentic Workflows CLI extension

### Install the gh-aw Extension

```bash
gh extension install github/gh-aw
```

Verify the installation:

```bash
gh aw --version
```

The exact version used by this repository's CI is pinned in
`.github/workflows/copilot-setup-steps.yml` (currently `v0.53.6`).  Use
that version when compiling workflows locally to ensure byte-for-byte
reproducible lock files.

```bash
gh extension install github/gh-aw@v0.53.6
```

### Clone and Explore

```bash
git clone https://github.com/steffenkoenig/agenti.git
cd agenti
```

Key files to review:

| Path | Purpose |
|------|---------|
| `.github/agents/*.agent.md` | Agent instruction files (the source of truth for agent behaviour) |
| `.github/workflows/*.md` | Workflow source files (human-readable, compiled to lock files) |
| `.github/workflows/*.lock.yml` | Compiled lock files (generated — do **not** edit by hand) |
| `.github/workflows/copilot-setup-steps.yml` | Environment bootstrap for GitHub Copilot Agent |
| `.gitattributes` | Marks `*.lock.yml` files as generated (`linguist-generated=true`) |

---

## Understanding the Architecture

This repository is **AI-native**: automated agents review the repository,
create issues, and implement those issues through pull requests — all without
human intervention.  There are two core workflows:

### `agenti-reviewer`

Runs on a schedule.  Audits the repository and creates GitHub Issues for any
improvements it finds.  Safe outputs: `create-issue` (max 10), `add-comment`
(max 10), `noop` (max 1).

### `issue-implementer`

Runs on a schedule.  Reads open GitHub Issues, prioritises them, and submits
pull requests with the required changes.  Safe outputs: `create-pull-request`
(max 5), `add-comment` (max 10), `noop` (max 1).

### How It All Fits Together

```
.github/agents/*.agent.md   ←  edit these to change agent behaviour
        │
        │ referenced by
        ▼
.github/workflows/*.md      ←  edit these to change workflow triggers / config
        │
        │ compiled by `gh aw compile`
        ▼
.github/workflows/*.lock.yml  ←  GENERATED — never edit directly
        │
        │ executed by GitHub Actions
        ▼
    GitHub Actions runner
```

The `.lock.yml` files are committed to the repository so that GitHub Actions
can execute them, but they are always derived from the `.md` sources.
`.gitattributes` marks them as generated so that GitHub hides them in diffs.

---

## Making Changes to Agent Instructions

> ⚠️ **Important:** Modifying agent instructions has non-obvious cascading
> effects.  An agent that reviews the repo may create issues that an
> implementing agent then acts on.  Read this section carefully before editing
> any instruction file.

### Where Agent Instructions Live

- **Agent personality / behaviour**: `.github/agents/<name>.agent.md`
- **Workflow configuration** (triggers, permissions, safe-outputs):
  `.github/workflows/<name>.md`

### Edit the `.md` Source, Never the `.lock.yml`

The `.lock.yml` files are **generated artefacts**.  Any direct edits will be
overwritten the next time `gh aw compile` is run.  Always:

1. Edit the relevant `.md` file.
2. Compile the lock file (see [Compiling Workflows](#compiling-workflows)).
3. Commit **both** the `.md` and the updated `.lock.yml` together.

### Changing Safe-Output Limits

Safe-output limits are declared in the workflow frontmatter
(`.github/workflows/<name>.md`).  They cap how many actions an agent can take
in a single run.  Increasing limits raises the blast radius of a misbehaving
agent — do so deliberately.

---

## Compiling Workflows

After editing a `.md` workflow source, regenerate its lock file:

```bash
# Compile a specific workflow
gh aw compile issue-implementer

# Compile all workflows
gh aw compile

# Compile and validate the output
gh aw compile --validate
```

Always commit the updated `.lock.yml` alongside the `.md` change.  A PR that
modifies a `.md` without updating the corresponding `.lock.yml` will break the
automated workflow cycle.

### Dependabot PRs

If Dependabot opens a PR that modifies generated manifest files
(`.github/workflows/package.json`, `.github/workflows/requirements.txt`,
`.github/workflows/go.mod`), **do not merge it directly**.  Instead:

1. Update the dependency version in the relevant `.md` source file.
2. Run `gh aw compile --dependabot` to bundle all fixes.
3. Open a new PR with the compiled changes.

---

## Testing Changes

There is currently no automated test suite for agent instructions.  Validate
your changes manually:

1. **Dry-run locally** — Use `gh aw compile --validate` to catch syntax errors
   in workflow files before pushing.
2. **Review the diff** — Inspect the generated `.lock.yml` diff to confirm only
   expected changes appear.
3. **Trigger via `workflow_dispatch`** — Both workflows support manual dispatch
   from the GitHub Actions tab.  Use this to verify behaviour without waiting
   for the scheduled run.
4. **Check run logs** — Use `gh aw logs <workflow-name>` or the GitHub Actions
   UI to review execution output.

---

## PR Process

### Branch Naming

```
<type>/issue-<number>-<short-description>
```

Examples:
- `fix/issue-12-missing-permissions`
- `feat/issue-34-new-triage-workflow`
- `docs/issue-56-contributing-guide`

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description> (#<issue-number>)
```

Common types: `fix`, `feat`, `docs`, `chore`, `refactor`.

### What to Include in Every PR

- A reference to the issue being resolved (`Closes #<number>`).
- Both the `.md` source **and** the compiled `.lock.yml` if any workflow was
  changed.
- A brief description of the change and its expected effect on agent behaviour.

### Review Requirements

- At least one human review for changes to agent instructions or safe-output
  limits.
- The automated `agenti-reviewer` workflow may also leave comments — address
  any concerns it raises before merging.

---

## AI-Specific Guidelines

### Writing Clear Agent Instructions

- Use imperative sentences: *"Fetch all open issues"*, not *"The agent should
  fetch open issues"*.
- Be explicit about what the agent **must not** do (e.g. *"Do not close issues
  directly"*).
- Group related instructions under clearly labelled headings.
- State acceptance criteria so the agent can self-verify.

### Token Efficiency

- Avoid repeating context that is already available through tools (e.g. file
  contents, issue body).
- Keep instruction files focused — one agent, one responsibility.
- Prefer numbered lists over prose for procedural steps.

### Minimising Blast Radius

- Keep `max` values for safe outputs as low as practical.
- When experimenting with a new agent behaviour, test with a reduced `max`
  first, then raise it once the behaviour is confirmed safe.
- Use `concurrency` groups (already set in both workflows) to prevent
  overlapping runs from compounding mistakes.
