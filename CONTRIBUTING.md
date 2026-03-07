# Contributing to agenti

Thank you for contributing! This document covers the conventions used in this repository.

## Editing Workflows

The `.lock.yml` files under `.github/workflows/` are **auto-generated** by `gh aw compile` and must not be edited by hand. To change a workflow:

1. Edit the corresponding `.md` source file (e.g. `.github/workflows/agenti-reviewer.md`).
2. Recompile:
   ```bash
   gh aw compile
   ```
3. Commit both the `.md` source and the regenerated `.lock.yml` together.

## Handling Dependabot PRs for Lock Files

Dependabot automatically opens PRs to update pinned GitHub Actions SHAs referenced in workflows. Because the `.lock.yml` files are generated, a Dependabot PR that touches a source workflow will require a recompile step:

1. Check out the Dependabot branch locally.
2. Apply the updated action version to the appropriate `.md` source file.
3. Recompile with the Dependabot flag:
   ```bash
   gh aw compile --dependabot
   ```
4. Commit the updated `.md` source and the regenerated `.lock.yml`, then push to the Dependabot branch.

This bundles the source change and the compiled output into a single commit so CI stays green.
