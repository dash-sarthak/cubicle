# AGENT.md

Instructions for coding agents working in this repo.

## Project

Cubicle — an agent orchestration platform (AMS). Teams bring LLM keys; Cubicle runs the SDLC behind tiered human gates. See `README.org` for the thesis and `PLAN.md` for current scope.

## Ground rules

- Read `PLAN.md` before proposing work. The MVP definition is the scope filter — features that don't serve the core loop are out until the loop ships.
- Core loop is the product: repo → spec → implement → test → tiered gate → merged PR.
- Keep the stack boring. Fewest files, shortest working diff.
- Non-trivial logic ships with one runnable check (assert-based or single small test). No frameworks.
- RBAC/access scoping is enforced by spec, not convention — never implement access checks as ad-hoc `if` statements scattered at call sites.

## Status

- Stack: Python 3.12+, OpenAI SDK, Docker sandbox, GitHub via PAT (decided — see `PLAN.md`)
