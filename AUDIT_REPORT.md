# 🔍 Repository Sentinel Audit Report

**Repository:** `steffenkoenig/agenti`  
**Audit Date:** 2025-03-06  
**Auditor:** Repository Sentinel (agenti-reviewer)  

---

## Executive Summary

This is a minimal **meta-infrastructure repository** built on GitHub Agentic Workflows (gh-aw).

**Critical Findings:** 3 | **Warnings:** 7 | **Enhancements:** 3 | **Self-Improvement:** 3

---

## File Structure Map

```
agenti/
├── README.md                              ← CRITICAL: Placeholder only ("# agenti")
├── .gitattributes                         ← Lock files marked as generated
├── .github/
│   ├── agents/
│   │   ├── agenti-reviewer.md             ← Agent: Repository Sentinel  
│   │   ├── issue-implementer.agent.md     ← Agent: Issue Implementer
│   │   └── agentic-workflows.agent.md     ← Agent: Workflow Dispatcher
│   └── workflows/
│       ├── issue-implementer.md           ← Workflow: auto-runs every 2 hours
│       ├── issue-implementer.lock.yml     ← Compiled (DO NOT EDIT manually)
│       └── copilot-setup-steps.yml        ← Environment setup
└── .vscode/
    ├── settings.json                      ← Copilot markdown enabled
    └── mcp.json                           ← gh-aw MCP server config
```

---

## GitHub Issues

---

### Issue #1: [Documentation] README.md is a Non-Functional Placeholder

**Description:**  
The README.md contains only `# agenti`. For a repository whose entire value is agentic infrastructure, this is the most critical documentation gap. Any developer or AI agent attempting to understand the repository's purpose will find zero guidance.

**Impact:** Critical

**Relations & Dependencies:**
- File: `README.md`
- Impacts all agents in `.github/agents/`
- Blocking: New contributors cannot onboard

**Proposed Solution:**
1. Add project description explaining this is an AI-native meta-repository
2. Add architecture section mapping agents to their roles
3. Add Getting Started section covering `gh aw` CLI setup
4. Document all three agents with trigger conditions and permissions
5. Document the `gh aw compile` workflow for updating lock files

**Acceptance Criteria:**
- [ ] README has project description (at least 3 sentences)
- [ ] README lists all agents with purpose, trigger, and permissions
- [ ] README documents the `gh aw compile` workflow
- [ ] README includes Getting Started section for new contributors

---

### Issue #2: [Automation] agenti-reviewer Has No Automated Trigger Workflow

**Description:**  
The `agenti-reviewer` agent exists in `.github/agents/agenti-reviewer.md` but there is NO corresponding workflow file (`.github/workflows/agenti-reviewer.md`) to automate its execution. The reviewer only runs when manually invoked — defeating its purpose as an autonomous sentinel. The `issue-implementer` runs every 2 hours automatically; the reviewer should also have a schedule.

**Impact:** Critical

**Relations & Dependencies:**
- Agent: `.github/agents/agenti-reviewer.md`
- Missing: `.github/workflows/agenti-reviewer.md`
- Missing: `.github/workflows/agenti-reviewer.lock.yml`
- Pattern: `issue-implementer.md` (follow this pattern)

**Proposed Solution:**
1. Create `.github/workflows/agenti-reviewer.md` with weekly schedule
2. Include `issues: write` permission in safe-output section
3. Set `create_issue: max: 20` in safe-outputs
4. Run `gh aw compile agenti-reviewer` to generate lock file

**Acceptance Criteria:**
- [ ] `.github/workflows/agenti-reviewer.md` created with weekly schedule
- [ ] `.github/workflows/agenti-reviewer.lock.yml` compiled and committed
- [ ] Workflow has `issues: write` permission
- [ ] Manual `workflow_dispatch` trigger included

---

### Issue #3: [Configuration] PR Safe-Output Cap (max:5) Conflicts with Agent's 10-Issue Promise

**Description:**  
`issue-implementer.md` declares `create-pull-request: max: 5` but the agent instructions say "Implement at most **10 issues** per run." The agent will consume tokens processing issues 6-10 but fail silently when attempting to create PRs beyond the cap.

**Impact:** Warning

**Relations & Dependencies:**
- Workflow: `.github/workflows/issue-implementer.md` (has `max: 5`)
- Agent: `.github/agents/issue-implementer.agent.md` (says "up to 10")
- Lock file: must be recompiled after change

**Proposed Solution:**
Option A (Recommended): Increase safe-output cap to match agent promise:
```yaml
safe-outputs:
  create-pull-request:
    max: 10
  add-comment:
    max: 20
```
Option B: Reduce agent promise to 5 issues per run.

**Acceptance Criteria:**
- [ ] `create-pull-request: max` matches agent's stated issue limit
- [ ] Lock file recompiled after change
- [ ] README documents true throughput

---

### Issue #4: [Security] copilot-setup-steps.yml Uses Unpinned Action Tag

**Description:**  
`copilot-setup-steps.yml` uses `actions/checkout@v6` — an unpinned mutable tag. This is a supply-chain security risk. The compiled lock file correctly uses pinned SHAs (e.g., `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2`), demonstrating awareness of this best practice but inconsistent application.

**Impact:** Warning

**Relations & Dependencies:**
- File: `.github/workflows/copilot-setup-steps.yml`
- Pattern to follow: `.github/workflows/issue-implementer.lock.yml` (uses pinned SHA)

**Proposed Solution:**
1. Update `copilot-setup-steps.yml`:
   ```yaml
   uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
   ```
2. Also pin `github/gh-aw/actions/setup-cli@v0.53.6` if SHA is available

**Acceptance Criteria:**
- [ ] `actions/checkout` uses full commit SHA with version comment
- [ ] `github/gh-aw/actions/setup-cli` is pinned or documented why it cannot be
- [ ] Dependabot configured to keep pinned SHAs updated (see Issue #12)

---

### Issue #5: [Agent Quality] agenti-reviewer Lacks Clean-State noop Instruction

**Description:**  
`agenti-reviewer.md` has no guidance for when the repository is in good health. Without a clean-state instruction, the agent may fabricate minor issues or loop indefinitely. The `issue-implementer.agent.md` handles this correctly: "If no actionable issues are found, call the `noop` safe-output tool."

**Impact:** Warning

**Relations & Dependencies:**
- Agent: `.github/agents/agenti-reviewer.md`
- Good Pattern: `.github/agents/issue-implementer.agent.md` (has noop handling)
- Related: Issue #2 (workflow must also handle noop in safe-outputs)

**Proposed Solution:**
Add to `agenti-reviewer.md` before the Output Format section:
```markdown
## Clean State Protocol
If after thorough review the repository has no actionable improvements:
1. Call the `noop` safe-output tool: "Repository is in good health. No improvements identified."
2. Do NOT fabricate issues to justify the run.

Deduplication: Check open issues and PRs before filing. Skip findings already tracked.
```

**Acceptance Criteria:**
- [ ] `agenti-reviewer.md` contains explicit noop instruction
- [ ] Deduplication check against open issues/PRs added
- [ ] Fabricating issues explicitly prohibited

---

### Issue #6: [Agent Quality] issue-implementer Tools Contradict Instructions (close_issue)

**Description:**  
`issue-implementer.agent.md` lists `close_issue` in its `tools:` frontmatter, but its instructions explicitly state: "Do not open or close issues directly." The agent has a capability it's instructed never to use, creating AI model confusion and unnecessary token consumption.

**Impact:** Warning

**Relations & Dependencies:**
- Agent: `.github/agents/issue-implementer.agent.md`
- Conflict: `tools: [..., close_issue, ...]` vs instruction "Do not open or close issues"
- Note: `agenti-reviewer.md` has the same contradiction

**Proposed Solution:**
Remove `close_issue` from the `tools:` list, OR update instructions to explicitly document when closing is appropriate.

**Acceptance Criteria:**
- [ ] No contradiction between tool list and written instructions
- [ ] Same fix applied to `agenti-reviewer.md` if it has the same issue
- [ ] If `close_issue` is intentionally kept: explicit criteria for its use added

---

### Issue #7: [Infrastructure] Missing .github/CODEOWNERS for Critical Agent Files

**Description:**  
No `.github/CODEOWNERS` file exists. Agent files in `.github/agents/` are critical infrastructure — a PR silently modifying the issue-implementer's behavior could bypass review. Without CODEOWNERS, there's no automated enforcement of review for these high-impact files.

**Impact:** Warning

**Relations & Dependencies:**
- Files to protect: `.github/agents/*.md`, `.github/workflows/*.md`
- Dependency: Branch protection must be enabled for CODEOWNERS to be enforced

**Proposed Solution:**
1. Create `.github/CODEOWNERS`:
   ```
   * @steffenkoenig
   .github/agents/ @steffenkoenig
   .github/workflows/*.md @steffenkoenig
   .github/workflows/*.lock.yml @steffenkoenig
   ```
2. Enable branch protection on `main` with required CODEOWNERS review

**Acceptance Criteria:**
- [ ] `.github/CODEOWNERS` created
- [ ] Branch protection enabled on `main`
- [ ] PR modifying `.github/agents/` auto-assigns owner as reviewer

---

### Issue #8: [Infrastructure] Missing GitHub Issue Templates

**Description:**  
No `.github/ISSUE_TEMPLATE/` directory exists. Since `agenti-reviewer` creates issues and `issue-implementer` processes them, issue quality directly impacts agent performance. Without templates, issues lack the structured fields the agents need.

**Impact:** Enhancement

**Relations & Dependencies:**
- Agent: `.github/agents/agenti-reviewer.md` (output format should match templates)
- Agent: `.github/agents/issue-implementer.agent.md` (reads issues to implement)

**Proposed Solution:**
1. Create `.github/ISSUE_TEMPLATE/improvement.md` matching agenti-reviewer's output format
2. Create `.github/ISSUE_TEMPLATE/bug_report.md`
3. Create `.github/ISSUE_TEMPLATE/config.yml` to disable blank issues

**Acceptance Criteria:**
- [ ] At least 2 issue templates exist (bug, improvement)
- [ ] Templates match format expected by issue-implementer
- [ ] Blank issues disabled via `config.yml`

---

### Issue #9: [Agent Quality] agentic-workflows.agent.md Hardcodes Version v0.53.6 in 7+ Places

**Description:**  
`agentic-workflows.agent.md` references version `v0.53.6` in 7+ external URL locations. When gh-aw releases a new version, all these references become stale simultaneously. There's no documented update process or version management.

**Impact:** Warning

**Relations & Dependencies:**
- Agent: `.github/agents/agentic-workflows.agent.md`
- Related files: `.github/workflows/copilot-setup-steps.yml`, `issue-implementer.lock.yml`

**Proposed Solution:**
1. Add version constant comment at top of file
2. Create `scripts/update-ghaw-version.sh` for atomic version upgrades
3. Document upgrade process in README

**Acceptance Criteria:**
- [ ] Version comment added at top of agent file
- [ ] Update script created
- [ ] All 3 version-bearing files updated atomically during upgrades

---

### Issue #10: [Agent Quality] agenti-reviewer Has No Scope Limits — Risk of Over-Auditing

**Description:**  
`agenti-reviewer.md` instructs the agent to audit "the entire repository" with no scope limits. Without constraints, the agent may spend tokens on generated files, external dependencies, or file 50+ low-priority issues that overwhelm the issue-implementer.

**Impact:** Warning

**Relations & Dependencies:**
- Agent: `.github/agents/agenti-reviewer.md`
- Downstream impact: `issue-implementer` overwhelmed by too many issues

**Proposed Solution:**
Add scope constraints to `agenti-reviewer.md`:
- Skip generated files (`*.lock.yml`, `node_modules/`)
- Priority ordering: Critical → Warning → Enhancement
- Issue cap: 15 per run maximum
- Check existing issues before filing (deduplication)

**Acceptance Criteria:**
- [ ] Generated files explicitly excluded from audit scope
- [ ] Issue cap per run documented (max 15)
- [ ] Priority ordering instruction added
- [ ] Deduplication instruction added

---

### Issue #11: [Infrastructure] No Dependabot Configuration for Action Version Updates

**Description:**  
The repository uses pinned action SHAs in the lock file but has no Dependabot configuration to keep them updated. Pinned SHAs will silently drift as Actions are patched. The `agentic-workflows.agent.md` even has a `dependabot` routing prompt — but it's never triggered because there's no config.

**Impact:** Enhancement

**Relations & Dependencies:**
- Agent: `.github/agents/agentic-workflows.agent.md` (has dependabot routing)
- Missing: `.github/dependabot.yml`
- Related: Issue #4 (unpinned actions)

**Proposed Solution:**
Create `.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
```

**Acceptance Criteria:**
- [ ] `.github/dependabot.yml` created with weekly schedule
- [ ] README documents Dependabot + gh-aw compile process

---

### Issue #12: [Infrastructure] Sparse Checkout References Non-Existent .agents Folder

**Description:**  
`issue-implementer.lock.yml` includes `.agents` in its sparse checkout, but this repo stores agents at `.github/agents/`. The `.agents` checkout silently succeeds with empty results — wasteful and confusing for future maintainers.

**Impact:** Enhancement (Low Priority)

**Proposed Solution:**
Investigate if this is intentional (gh-aw convention fallback) or a bug. If a bug, file upstream with `github/gh-aw`. Document agent file location in README.

**Acceptance Criteria:**
- [ ] Investigation completed and documented
- [ ] If upstream bug: issue filed with `github/gh-aw`
- [ ] README documents where agent files live

---

## Recursive Evolution

### Self-Audit: What Did I Struggle With?

1. **No Write Permissions:** Ran with `issues: read` only — cannot create GitHub Issues directly. This audit is committed as a file instead. The agenti-reviewer workflow (Issue #2) must include `issues: write`.

2. **Infrastructure-Only Repo:** Core instructions assume application code exists (algorithms, tests, etc.). A repository type detection protocol is needed in the agent instructions.

3. **Sandboxed Environment:** External URL validation was impossible. Instructions should acknowledge this limitation.

**Recommended Fix:** Add to `agenti-reviewer.md`:
```markdown
## Repository Type Detection
- Application repo (has src/, *.py/*.ts/*.go): Apply code quality + testing audits
- Infrastructure repo (.github/agents/ only): Focus on prompt quality + workflow reliability
- Mixed: Apply both
```

### New Agent Proposals

**`security-sentinel`:** Dedicated supply chain security auditor (action pinning, permissions, CODEOWNERS, branch protection). 33% of this audit's findings were security-related — justifying a specialist.

**`doc-guardian`:** Documentation health specialist (README completeness, changelog, template enforcement). Prevents documentation debt from accumulating after each merged PR.

---

### Issue #13: [Self-Improvement] agenti-reviewer Needs issues:write Permission to Function

**Description:** The agent's core purpose is creating GitHub Issues but it has no workflow granting `issues: write`. Without this, it produces findings but cannot act on them.

**Impact:** Critical

**Acceptance Criteria:**
- [ ] agenti-reviewer workflow created with `issues: write`
- [ ] Agent has fallback behavior (commit to AUDIT_REPORT.md) when lacking write permission
- [ ] Permission requirement documented in agent frontmatter

---

### Issue #14: [Self-Improvement] agenti-reviewer Lacks Repository Type Detection Logic

**Description:** Agent assumes application code repository. For infrastructure/agent repos, audit categories should shift to prompt quality, workflow reliability, and permission hygiene.

**Impact:** Warning

**Acceptance Criteria:**
- [ ] Repository type detection added to `agenti-reviewer.md`
- [ ] Audit scope adapts based on detected repository type

---

### Issue #15: [Self-Improvement] Create security-sentinel Specialist Agent

**Description:** 4 of 12 findings (33%) are security-related. A dedicated monthly security sentinel would provide deeper, more consistent security monitoring.

**Impact:** Warning

**Acceptance Criteria:**
- [ ] `.github/agents/security-sentinel.md` created
- [ ] Monthly workflow created and compiled
- [ ] Security checklist covers supply chain, permissions, and secrets

---

### Issue #16: [Self-Improvement] Create doc-guardian Specialist Agent for Documentation Health

**Description:** Empty README (Issue #1) and documentation drift risk justify a PR-triggered documentation guardian agent.

**Impact:** Enhancement

**Acceptance Criteria:**
- [ ] `.github/agents/doc-guardian.md` created
- [ ] PR-merge triggered workflow created
- [ ] Agent validates README completeness on each merge

---

## Summary Table

| # | Category | Title | Impact |
|---|----------|-------|--------|
| 1 | Documentation | README.md is a placeholder | Critical |
| 2 | Automation | agenti-reviewer has no workflow | Critical |
| 3 | Configuration | PR cap (5) conflicts with 10-issue promise | Warning |
| 4 | Security | Unpinned action in copilot-setup-steps.yml | Warning |
| 5 | Agent Quality | agenti-reviewer lacks noop instruction | Warning |
| 6 | Agent Quality | issue-implementer close_issue contradiction | Warning |
| 7 | Infrastructure | Missing CODEOWNERS | Warning |
| 8 | Infrastructure | Missing Issue Templates | Enhancement |
| 9 | Agent Quality | agentic-workflows hardcoded version | Warning |
| 10 | Agent Quality | agenti-reviewer lacks scope limits | Warning |
| 11 | Infrastructure | No Dependabot configuration | Enhancement |
| 12 | Infrastructure | Sparse checkout references non-existent .agents | Enhancement |
| 13 | Self-Improvement | agenti-reviewer needs issues:write | Critical |
| 14 | Self-Improvement | agenti-reviewer lacks repo type detection | Warning |
| 15 | Self-Improvement | Create security-sentinel agent | Warning |
| 16 | Self-Improvement | Create doc-guardian agent | Enhancement |

*Generated by Repository Sentinel (agenti-reviewer)*
