#!/usr/bin/env python3
"""Validates that agent and workflow Markdown files have required frontmatter fields.

Agent files (.github/agents/*.md, *.agent.md):
  - Required: description
  - Required unless disable-model-invocation is true: name

Workflow markdown files (.github/workflows/*.md):
  - Required: name, on

Also verifies that every workflow .md file has a corresponding .lock.yml file.
"""

import glob
import os
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def parse_frontmatter(filepath):
    """Extract and parse YAML frontmatter from a Markdown file.

    Returns:
        dict   – parsed frontmatter on success
        None   – file has no frontmatter delimiters
        False  – frontmatter contains invalid YAML or a non-mapping value
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return None

    # Require the first non-empty line to be a frontmatter opening delimiter.
    start_index = None
    for idx, line in enumerate(lines):
        if line.strip() == "":
            continue
        if line.strip() == "---":
            start_index = idx
        break

    if start_index is None:
        return None

    # Find the closing delimiter line after the opening delimiter.
    end_index = None
    for idx in range(start_index + 1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break

    if end_index is None:
        return None

    frontmatter_str = "".join(lines[start_index + 1 : end_index]).strip()
    try:
        parsed = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError as exc:
        print(f"  ERROR: Invalid YAML frontmatter in {filepath}: {exc}")
        return False

    if parsed is None:
        return {}

    if not isinstance(parsed, dict):
        print(
            f"  ERROR: Frontmatter in {filepath} parsed to {type(parsed).__name__},"
            " expected a mapping."
        )
        return False

    return parsed


def check_agent_files():
    """Validate frontmatter in .github/agents/ markdown files."""
    errors = []

    agent_files = sorted(
        set(
            glob.glob(".github/agents/*.md")
            + glob.glob(".github/agents/**/*.md", recursive=True)
        )
    )

    for filepath in agent_files:
        fm = parse_frontmatter(filepath)

        if fm is False:
            errors.append(f"{filepath}: invalid YAML frontmatter")
            continue

        if fm is None:
            errors.append(f"{filepath}: missing frontmatter (no --- delimiters found)")
            continue

        if "description" not in fm:
            errors.append(
                f"{filepath}: missing required frontmatter field 'description'"
            )

        # name is required unless the file explicitly disables model invocation
        if not fm.get("disable-model-invocation"):
            if "name" not in fm:
                errors.append(
                    f"{filepath}: missing required frontmatter field 'name'"
                )

    return errors


def check_workflow_files():
    """Validate frontmatter in .github/workflows/*.md files."""
    errors = []

    workflow_files = sorted(glob.glob(".github/workflows/*.md"))

    for filepath in workflow_files:
        fm = parse_frontmatter(filepath)

        if fm is False:
            errors.append(f"{filepath}: invalid YAML frontmatter")
            continue

        if fm is None:
            errors.append(f"{filepath}: missing frontmatter (no --- delimiters found)")
            continue

        for field in ("name", "on"):
            # PyYAML (YAML 1.1) parses the bare key `on` as the boolean True
            # rather than the string "on". Accept either form.
            present = field in fm or (field == "on" and True in fm)
            if not present:
                errors.append(
                    f"{filepath}: missing required frontmatter field '{field}'"
                )

    return errors


def check_lock_file_consistency():
    """Verify that every workflow .md has a corresponding .lock.yml."""
    errors = []

    workflow_md_files = sorted(glob.glob(".github/workflows/*.md"))

    for filepath in workflow_md_files:
        lock_path = filepath[: -len(".md")] + ".lock.yml"
        if not os.path.exists(lock_path):
            errors.append(
                f"{filepath}: missing corresponding lock file '{lock_path}'"
            )

    return errors


def main():
    # Run from repository root
    repo_root = os.path.join(os.path.dirname(__file__), "..", "..")
    os.chdir(repo_root)

    all_errors = []

    print("Checking agent frontmatter (.github/agents/)...")
    agent_errors = check_agent_files()
    for err in agent_errors:
        print(f"  ✗ {err}")
    all_errors.extend(agent_errors)

    print("Checking workflow frontmatter (.github/workflows/*.md)...")
    workflow_errors = check_workflow_files()
    for err in workflow_errors:
        print(f"  ✗ {err}")
    all_errors.extend(workflow_errors)

    print("Checking lock file consistency...")
    lock_errors = check_lock_file_consistency()
    for err in lock_errors:
        print(f"  ✗ {err}")
    all_errors.extend(lock_errors)

    if all_errors:
        print(f"\n✗ {len(all_errors)} validation error(s) found.")
        sys.exit(1)
    else:
        print("\n✓ All frontmatter and lock-file consistency checks passed.")


if __name__ == "__main__":
    main()
