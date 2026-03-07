# GitHub Copilot Instructions

This file provides editor-level hints for GitHub Copilot when assisting with code in this repository.

## Style & Conventions

- Use clear, unambiguous language in agent instruction files (`.github/agents/*.md`).
- Keep agent prompts atomic — each constraint or skill should have a single, clear purpose.
- Follow the existing frontmatter convention for agent files: `name:`, `description:`, `tools:`.
- Workflow source files live in `.github/workflows/*.md`; compiled lock files (`.lock.yml`) are auto-generated — do not suggest edits to lock files directly.
- Prefer minimal permissions in workflow definitions (`contents: read` unless elevated access is explicitly required via `safe-outputs`).

## Repository Context

- Agent instruction files: `.github/agents/`
- Workflow source files: `.github/workflows/*.md`
- Compiled workflows (do not edit): `.github/workflows/*.lock.yml`
- All pull requests require human review before merging — no automated merges occur.
