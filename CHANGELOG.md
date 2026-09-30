# Changelog

All notable changes to Cubicle.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Project scaffold: uv-managed `cubicle` package with module stubs per PLAN.md (cli, config, github, llm, sandbox, agents, pipeline).
- BDD harness (pytest-bdd 9): config scenario green; core-loop scenario red at `pipeline.run` as the intent test for build order step 2.
- Tooling gates: ruff format/lint (2-space indent), ty type check, Makefile (`make check`), `.env.example`, `.gitignore`.

### Decided

- pytest-bdd over behave (single runner, fixture DI, pytest-dev maintenance); SQLite deferred until state outgrows files.
- `README.org`: product thesis — BYOK agent orchestration platform for startups, tiered human gates, role triage, build order.
- `PLAN.md`: living plan; MVP draft and milestones.
- `AGENT.md`: ground rules for coding agents working in this repo.
- v0 stack decisions: Python + OpenAI SDK, PAT-based repo access, Docker sandbox (see `PLAN.md`).
- MVP build spec: pipeline stages, module layout, trust-boundary rule, build order (see `PLAN.md`).
