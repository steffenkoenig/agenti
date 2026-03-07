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

Dependabot automatically opens PRs to update pinned GitHub Actions SHAs referenced in workflows by editing the generated `.lock.yml` files under `.github/workflows/`.

In this repository, the `.md` workflow sources only contain gh-aw frontmatter/description and do **not** contain the actual `uses:` pins. The `.lock.yml` files are therefore the authoritative source of pinned SHAs for CI.

For a Dependabot PR that only changes `.lock.yml` files:

1. Review the proposed `.lock.yml` changes to ensure they look reasonable.
2. Do **not** edit the corresponding `.md` workflow source files.
3. Do **not** re-run `gh aw compile` for these PRs, as that may overwrite Dependabot's updates.
4. If the changes are acceptable and CI is green, merge the PR.

If in the future a Dependabot PR (or a manual change) modifies a `.md` workflow source file that actually contains action pins, then you should recompile to keep the lock files in sync:

1. Check out the branch locally.
2. Run:
   ```bash
   gh aw compile --dependabot
   ```
3. Commit the updated `.md` source and the regenerated `.lock.yml` together, then push the branch.
