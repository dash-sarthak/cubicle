# AGENT.md

Instructions for coding agents working in this repo.

## Project

Cubicle — an agent orchestration platform (AMS). Teams bring LLM keys; Cubicle runs the SDLC behind tiered human gates. See `README.md` for the thesis and `PLAN.md` for current scope.

## Ground rules

- Read `PLAN.md` before proposing work. The MVP definition is the scope filter — features that don't serve the core loop are out until the loop ships.
- Core loop is the product: repo → spec → implement → test → tiered gate → merged PR.
- Keep the stack boring. Fewest files, shortest working diff.
- Operational commands and failure modes live in `RUNBOOK.md`; update it in the same commit that changes them.
- Non-trivial logic ships with one runnable check (assert-based or single small test). No frameworks.
- RBAC/access scoping is enforced by spec, not convention — never implement access checks as ad-hoc `if` statements scattered at call sites.

## Workflow

Every work item ships through the same loop (command procedure: `RUNBOOK.md` §1.3):

- Multi-commit work needs a GitHub issue first. An issue describes the work needed — the outcome or business requirement — never the code change. One-commit tasks get no issue.
- Branch per work item, even single commits: `feature|bug|improvement|infra/<issue_number>`; issueless tasks use `type/slug` (e.g. `improvement/runbook`).
- Tests come before changes: BDD red scenario first (see PLAN.md paradigm).
- Commit messages: `gh-<issue_number>: <what changed>`; issueless: `<type>: <what changed>`.
- CI on GitHub gates the PR; after green, the CHANGELOG.md entry lands on the branch, then merge to main and delete the branch.
- Intermediate session state lives in `STATE.md` (repo root, gitignored, never committed).

## Conventions

- Data shapes are pydantic models; `cubicle/models.py` owns the shapes shared by real services and their test fakes. Validate external input with pydantic where it enters the program, not with hand-rolled checks.
- Names and docstrings say exactly what a thing does, at its own level of abstraction. No jargon: a module that loads keys says it loads keys.
- Configuration comes from a `.env` file (BYOK); see `.env.example`.
- No banner/section comments (`# --- foo ---`). Comment only where the code cannot explain itself; docstrings for public shapes are fine.
- 80-character lines.
- Never-nester: guard clauses and negative checks over nesting. Flatten before you add a level.

## Status

- Stack: Python 3.12+, OpenAI SDK, Docker sandbox, GitHub via PAT (decided — see `PLAN.md`)
