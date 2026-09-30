# PLAN

Living plan for Cubicle. Decisions land here first.

## Goal

Prove the loop: **repo → spec → implement → test → tiered gate → merged PR** — on a real repo, with a real human gate.

## MVP (decided)

Thinnest slice that runs the loop end to end:

- Single repo, single LLM provider, BYOK via local config file (no vault, no billing)
- Entry point: point Cubicle at an issue → it produces a PR with spec, implementation, and test results attached
- Tests run in an isolated sandbox; results go into the PR
- Gate = GitHub PR review. No gate UI — GitHub *is* the gate UI.
- v0 gates everything through a human; tiered auto-merge is M1, not MVP.

### How (the build)

One command, one PR:

```bash
cubicle run --repo owner/name --issue 42
```

Pipeline stages:

1. **Fetch** — shallow-clone the repo (git CLI), pull the issue (GitHub REST via PAT).
2. **Spec** — one OpenAI call with issue + `git ls-files` + README → structured spec: goal, approach, files to touch, acceptance criteria.
3. **Implement** — tool loop on a branch (`cubicle/issue-42`): `read_file`, `write_file`, `list_files`. File tools only.
4. **Test** — write tests, then `docker run --rm -v worktree:/src image pytest` in the sandbox. Network in-container: package registry only.
5. **Ship** — commit, push, open PR. Body carries the spec summary + full test output.
6. **Gate** — human merges on GitHub.

**Trust boundary (hard rule):** the host never executes agent-generated code. Implementation runs through file tools only; execution happens exclusively inside the Docker sandbox. This is the seed of the RBAC thesis.

Module layout (5 files, flat package `cubicle/`):

- `cli.py` — arg parsing, entry point
- `config.py` — `.env` loader (GITHUB_PAT, OPENAI_API_KEY, CUBICLE_MODEL)
- `github.py` — issue fetch, PR creation (httpx); git ops via git CLI
- `llm.py` — OpenAI wrapper: tool loop, structured output, token accounting
- `sandbox.py` — docker run wrapper: exit code + captured output

Stage functions (spec / implement / test) get written into `llm.py`/`pipeline.py` at build step 2, wherever they actually land — no speculative agents module.

Guards: tool loop capped (max ~30 iterations), token spend logged per run, any stage crash exits non-zero with the stage name — v0 resume semantics are "re-run".

Build order (riskiest first):

1. Skeleton: config + CLI + GitHub client (fetch a real issue)
2. `llm.py` tool loop + implement agent on a local repo, tests run on host (temporary)
3. Swap in Docker sandbox
4. Spec agent + PR assembly (push + open PR with body)
5. Dogfood: 10 real issues → success criteria

### Out of scope for MVP

Dashboard, founder view, depth toggle, RBAC UI, multi-tenancy, billing, reporting agents, agent personas beyond the loop.

### Success criteria

1. 10 real issues from a real repo → 10 PRs opened
2. The gate catches at least one real bug (proof the gate matters)
3. The human running it wants to run it again next week

## Milestones

- **M0 — Loop**: issue in → PR out, all-human gate (MVP)
- **M1 — Tiers**: blast-radius tiering + RBAC scopes; low-risk auto-merge
- **M2 — Trust surface**: dashboard v1 (pipeline status, spend per agent, gate queue)

## Decided (v0)

- **Stack**: Python 3.12+, OpenAI SDK (`openai`), own tool-use loop — no agent framework.
- **Repo access**: GitHub PAT in local config; GitHub App is an M1+ upgrade when org installs are needed.
- **Sandbox**: one `docker run` per pipeline execution; no network except the package registry.
- **Provider**: OpenAI only in v0; multi-provider BYOK waits for a second customer.
- **BDD framework**: pytest-bdd 9, over behave — one runner for unit + BDD, fixture `target_fixture` DI for fake LLM/GitHub/sandbox, active pytest-dev maintenance (v9.0.0). behave would fork the toolchain into a second runner with no parallelism story. Paradigm: BDD → tests → code; no code without a red scenario.
- **Tooling**: ruff (format + lint, 2-space indent), mypy strict as the type gate (`make type`); ty stays installed for editor LSP only. Makefile gates (`make check` = lint + type + test). SQLite reserved for when state outgrows files — not before.

Config shape: `.env` (GITHUB_PAT, OPENAI_API_KEY) + repo/target arguments on the CLI.

## Open decisions

- (none currently — everything above is decided; new forks land here first)

## Status

Scaffold committed. Suite state: config scenario green (thin slice), core-loop scenario red at `pipeline.run` — the intent test for build order step 2.
