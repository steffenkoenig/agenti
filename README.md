# agenti

A self-improving, AI-native meta-repository that hosts autonomous agentic workflows for automated software engineering. This repository IS the infrastructure — it contains no application code, only the AI agents and GitHub workflows that continuously improve themselves and other repositories.

## Architecture

```
agenti/
├── .github/agents/                   # Agent definitions (prompts + tools)
│   ├── agenti-reviewer.md            # Repository Sentinel: audits repos, files issues
│   ├── issue-implementer.agent.md    # Issue Implementer: resolves issues via PRs
│   └── agentic-workflows.agent.md    # Workflow Dispatcher: routes workflow tasks
└── .github/workflows/                # Automated triggers
    ├── issue-implementer.md          # Runs every 2 hours: picks top 10 issues → PRs
    ├── issue-implementer.lock.yml    # Compiled workflow (auto-generated, do not edit)
    └── copilot-setup-steps.yml       # GitHub Copilot environment setup
```

## Agents

| Agent | Schedule | Purpose | Max Output |
|-------|----------|---------|------------|
| `issue-implementer` | Every 2 hours | Implements up to 10 open GitHub Issues as pull requests | 5 PRs / run |
| `agenti-reviewer` | Manual (no workflow yet — see Issue #2) | Audits the repo and files improvement issues | 20 issues / run |
| `agentic-workflows` | On-demand | Dispatcher for creating/debugging/upgrading gh-aw workflows | N/A |

## Getting Started

### Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated
- [gh-aw extension](https://github.com/github/gh-aw) v0.53.6+

```bash
# Install gh-aw
gh extension install github/gh-aw

# Verify installation
gh aw --version
```

### Updating Workflows

Agent workflows are defined in `.github/workflows/*.md` and compiled to `.lock.yml` files.
**Never edit the `.lock.yml` files directly.**

```bash
# After editing issue-implementer.md, recompile:
gh aw compile issue-implementer

# Validate the compiled output:
gh aw compile --validate
```

### Upgrading gh-aw Version

When upgrading to a new gh-aw version, update all version references atomically:

1. Update version in `.github/workflows/copilot-setup-steps.yml`
2. Update version in `.github/agents/agentic-workflows.agent.md` (has 7+ version references)
3. Recompile all workflows: `gh aw compile`

## How It Works

1. The **issue-implementer** workflow triggers on a schedule (every 2 hours) on `main`
2. It fetches all open GitHub Issues, prioritizes them by labels/reactions/age
3. It implements the top issues (up to 5 PRs per run)
4. The **agenti-reviewer** (when triggered manually) audits the repository and files new issues
5. The cycle continues: audit → issue → implement → PR → merge

## Contributing

- Agent definitions live in `.github/agents/` — markdown files with YAML frontmatter
- Workflow sources live in `.github/workflows/*.md` — always run `gh aw compile` after editing
- Lock files (`*.lock.yml`) are auto-generated — never edit manually
- Branch protection on `main` requires pull request reviews
- Critical agent and workflow files require owner approval (see CODEOWNERS)

## Open Improvement Issues

See [AUDIT_REPORT.md](./AUDIT_REPORT.md) for the full list of identified improvements,
or check the GitHub Issues tab for actionable items.
