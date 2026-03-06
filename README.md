# agenti

> A self-managing GitHub repository powered by autonomous AI agent workflows.

**agenti** uses [GitHub Agentic Workflows (gh-aw)](https://github.com/github/gh-aw) to continuously review its own code, file improvement issues, and implement fixes — all without manual intervention.

## What it does

| Agent | Trigger | Action |
|-------|---------|--------|
| `agenti-reviewer` | Scheduled | Reviews the repository, identifies improvements, and files GitHub Issues |
| `issue-implementer` | Every 2 hours | Picks the top 5 open issues by priority, implements them, and opens pull requests |

The repository is essentially **self-improving**: the reviewer finds problems, the implementer fixes them, and humans can review and merge the resulting PRs.

## Architecture

```
.github/
  agents/
    agenti-reviewer.md          # Reviewer agent instructions
    agentic-workflows.agent.md  # Dispatcher for gh-aw workflow tasks
    issue-implementer.agent.md  # Implementer agent instructions
  workflows/
    issue-implementer.md        # Workflow source (schedule, permissions, safe-outputs)
    issue-implementer.lock.yml  # Compiled lock file (generated — do not edit)
    copilot-setup-steps.yml     # MCP server and tool setup for Copilot agents
```

### Key design principles

- **Safe-output limits**: Every workflow caps the number of GitHub API actions per run (e.g., max 5 PRs, max 10 comments) to prevent runaway automation.
- **Prompt injection defense**: Issue and PR bodies are treated as untrusted data — agents never follow instructions embedded in repository content.
- **Minimal permissions**: Each workflow declares only the GitHub token permissions it needs.
- **Idempotency**: Agents check for existing open PRs before implementing an issue to avoid duplicate work.

## Getting started

### Prerequisites

- A GitHub repository
- [GitHub Copilot](https://github.com/features/copilot) access (for the Copilot engine)
- [gh-aw CLI](https://github.com/github/gh-aw) (for local development and compiling workflows)

### Setup

1. **Clone or fork** this repository
2. **Enable GitHub Actions** in your repository settings
3. **Configure Copilot agent permissions** — ensure the workflow has access to create PRs and issues
4. The agents will start running on their configured schedules automatically

### Local development

```bash
# Install gh-aw CLI
gh extension install github/gh-aw

# Edit a workflow source file
vim .github/workflows/issue-implementer.md

# Compile to lock file after editing
gh aw compile issue-implementer

# Run a workflow locally (dry run)
gh aw run issue-implementer --dry-run
```

> ⚠️ Never edit `.lock.yml` files directly — they are generated and will be overwritten on the next compile.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on modifying agent instructions and workflow files.

## Security

See [SECURITY.md](SECURITY.md) for the vulnerability disclosure process and security considerations specific to autonomous AI agent repositories.

## License

This project is open source. See the repository for license details.
