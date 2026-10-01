# Runbook

Step-by-step procedures for routine operations, maintenance tasks, and
incident resolution on Cubicle. Every procedure ends with a verification
step; if verification fails, go to the matching incident in §3. Update a
procedure in the same commit that changes what it does.

## 1. Routine operations

### 1.1 Provision a workstation

1. `uv sync`
2. `cp .env.example .env`
3. Edit `.env`: set `GITHUB_PAT` and `OPENAI_API_KEY` to real values.
   `CUBICLE_MODEL` defaults to `gpt-4.1`.

Verify: `make check` — expect everything green, ending
`3 passed, 1 xfailed`; the xfail is the core-loop scenario, red by
design until build order step 2 (Incident 3.1).

### 1.2 Run the core loop (issue → PR)

1. Complete 1.1 first.
2. `uv run cubicle run --repo owner/name --issue 42`

Expected today: prints `#<n> <title>`, then stops non-zero with
`stopping before spec — build order step 2`. The fetch stage is real
(PAT auth, response validated into the shared Issue shape); spec,
implement, test, and ship are not built. Real-repo proof lands with
dogfooding (build order step 5).

### 1.3 Ship a work item

Rules in `AGENTS.md` → Workflow. Sequence:

1. Multi-commit work → GitHub issue first (states the outcome, never the
   code change); a workflow posts the solution template as the first
   comment automatically. First actionable: fill it in by editing the
   posted comment — every header kept, N/A where not required. One-commit
   task → skip this step.
2. `git checkout -b <type>/<issue-number-or-slug>` — type is `feature`,
   `bug`, `improvement`, or `infra`.
3. Write the failing test or scenario (red first — PLAN.md paradigm).
4. Change until `make check` matches the recorded baseline or better.
5. Commit: `gh-<issue_number>: <what changed>`; issueless:
   `<type>: <what changed>`.
6. `git push -u origin <branch>` and open a PR — the `PR: <url>` comment
   on the issue posts automatically. One shot: `scripts/ship-pr.sh
   <branch> <title> [body-file]`.
7. CI green → CHANGELOG.md entry under `[Unreleased]`, commit, push;
   CI runs again.
8. Merge the PR once the latest commit is green.
9. `git checkout main && git pull && git branch -d <branch>` and delete
   the remote branch — or one shot: `scripts/merge-pr.sh <branch>`.

Verify: PR merged, branch gone on both ends, `make check` on main
matches the recorded baseline.

## 2. Maintenance tasks

### 2.1 Reformat and autofix lint

1. `make fmt`

Verify: output ends `All checks passed!`; `git status` shows only the
files you intended to touch.

### 2.2 Update dependencies

1. `uv lock --upgrade`
2. `make check`

Verify: `make check` result matches the recorded baseline (Incident 3.1).
If a gate breaks, revert with `git checkout uv.lock` and upgrade
selectively.

### 2.3 Record a decision or status change

1. Edit `PLAN.md` (decisions, status) — not this file.
2. Add a `CHANGELOG.md` entry under `[Unreleased]`.

Verify: `grep -n` finds the new line in both files.

## 3. Incident resolution

Format: symptom → diagnose → resolve.

### 3.1 Suite state vs the strict xfail

- Symptom: `1 passed, 1 xfailed` — that is the recorded baseline; no
  action.
- Symptom: suite fails with `XPASS(strict)` — `pipeline.run` started
  passing. Remove the xfail marker as part of build order step 2's own
  work item, never in a drive-by.
- Symptom: `1 failed` — regression or a stripped marker; fix before
  commit.

### 3.2 `make check` fails on lint

- Symptom: `make lint` exits nonzero with ruff findings.
- Diagnose: read the findings; if they describe formatting only, run 2.1.
- Resolve: `make fmt`, review the diff, re-run `make check`.

### 3.3 `make check` fails on types

- Symptom: `make type` (mypy strict) exits nonzero.
- Diagnose: the output names file, line, and missing annotation.
- Resolve: add the annotation; no `# type: ignore` without a comment
  naming why.

### 3.4 `cubicle run` raises `NotImplementedError`

- Symptom: `NotImplementedError: cli wiring: build order step 1`.
- Diagnose: expected until build order step 1 lands (`PLAN.md`).
- Resolve: none. Do not "fix" by implementing the pipeline inside an
  incident; wire it as planned work.

### 3.5 New incident

Any failure that costs more than a minute to diagnose gets a section
here: symptom → diagnose → resolve, three bullets each.
