# Changelog

All notable changes to Cubicle.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- AGENT.md renamed to AGENTS.md; file header and RUNBOOK.md §1.3 reference updated (one-commit task, no issue).
- README converted from Org to Markdown; status section now states the build state (#6).

- Conventions pass: pydantic everywhere (shared models `Issue`/`Spec`/`PRRecord` in `cubicle/models.py`; `Config` with env aliases + blank rejection), 80-column lines, banner comments removed, never-nester rule recorded in AGENT.md.
- Docstrings rewritten to say what each module, class, and function does in plain words; jargon ("seam") purged and the plain-naming rule recorded in AGENT.md.

- Type gate: mypy 2.3 strict (`make type`), hints everywhere including BDD fakes/steps; ty retained for editor LSP only. Dropped speculative `agents.py` stub — stage functions land with build step 2.

### Added

- Loop tooling: `scripts/ship-pr.sh` (push, open PR, watch CI) and `scripts/merge-pr.sh` (merge, delete branch, sync main) — canonical one-shot forms of RUNBOOK §1.3 steps 6–9; `.pr-body.md` gitignored for custom PR bodies (#14).
- Issue/PR automation: native issue template (blank issues disabled); workflows post the solution-template comment on new issues and the `PR: <url>` link on referenced issues; manual posting of both retired (#11).
- Issue discipline: solution-template comment (`.github/issue-solution-template.md`) is the first actionable on every issue; raising a PR posts a `PR: <url>` comment on the issue; PR links backfilled on #2/#4/#6 (#9).
- Issue fetch: `GitHubClient.get_issue` (httpx + PAT, response validated into the shared `Issue` shape at the boundary); `cubicle run` loads `.env`, fetches, shows the issue, stops non-zero naming the next stage (#4). Build order step 1 complete.
- CI gate: GitHub Actions runs `make check` (ruff, mypy strict, pytest, Python 3.12 floor) on every PR and push to main; actions pinned to commit SHAs (#2). Core-loop scenario strictly xfailed until build order step 2 lands.
- Dev workflow rules (AGENT.md) and ship-a-work-item procedure (RUNBOOK.md §1.3); STATE.md for intermediate session state (gitignored).
- Project scaffold: uv-managed `cubicle` package with module stubs per PLAN.md (cli, config, github, llm, sandbox, pipeline).
- BDD harness (pytest-bdd 9): config scenario green; core-loop scenario red at `pipeline.run` as the intent test for build order step 2.
- Tooling gates: ruff format/lint (2-space indent), ty type check, Makefile (`make check`), `.env.example`, `.gitignore`.

### Decided

- pytest-bdd over behave (single runner, fixture DI, pytest-dev maintenance); SQLite deferred until state outgrows files.
- `README.org`: product thesis — BYOK agent orchestration platform for startups, tiered human gates, role triage, build order.
- `PLAN.md`: living plan; MVP draft and milestones.
- `AGENT.md`: ground rules for coding agents working in this repo.
- v0 stack decisions: Python + OpenAI SDK, PAT-based repo access, Docker sandbox (see `PLAN.md`).
- MVP build spec: pipeline stages, module layout, trust-boundary rule, build order (see `PLAN.md`).
