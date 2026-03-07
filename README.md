# agenti

A self-improving GitHub repository powered by GitHub Copilot agentic workflows. **agenti** automatically audits itself for improvements, files issues, and implements those issues — all without human intervention.

## How It Works

Two agentic workflows run on a schedule and keep the repository healthy:

| Workflow | Schedule | What it does |
|---|---|---|
| **Agenti Reviewer** | Every 2 hours (configurable) | Audits the repository holistically and opens GitHub Issues for any improvements it finds |
| **Issue Implementer** | Every 2 hours (configurable) | Picks up open GitHub Issues, implements the changes, and opens pull requests |

The schedule is defined in the `on.schedule` frontmatter of each workflow `.md` source file (e.g. `.github/workflows/agenti-reviewer.md`). Edit the `schedule` field and recompile to change the cadence.

## Prerequisites

- A GitHub repository with **GitHub Copilot** enabled. Agentic workflows require a plan that includes GitHub Copilot (e.g. Copilot Business or Copilot Enterprise). See [GitHub's Copilot plans](https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot) for details.
- The [`gh-aw`](https://github.github.com/gh-aw/introduction/overview/) CLI extension installed locally if you want to edit or recompile workflows:
  ```bash
  gh extension install github/gh-aw
  ```

## Setup

1. **Fork or clone this repository** into your GitHub account or organization.

2. **Enable GitHub Copilot** for the repository (Settings → Copilot).

3. **Add the `COPILOT_GITHUB_TOKEN` repository secret** — go to **Settings → Secrets and variables → Actions → New repository secret** and add a token with GitHub Copilot access. Both workflows validate this secret at startup and will fail without it.

4. **Grant the required permissions** to the `GITHUB_TOKEN` used by the workflows. The compiled lock files already declare the minimum permissions needed (`contents`, `issues`, `pull-requests`).

5. The workflows run automatically on their schedule. You can also trigger them manually from the **Actions** tab using the `workflow_dispatch` event.

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

## Repository Structure

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on modifying agent instructions and workflow files.

## Security

See [SECURITY.md](SECURITY.md) for the vulnerability disclosure process and security considerations specific to autonomous AI agent repositories.

## License

No license has been specified for this project yet.
