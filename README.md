# Cubicle

The AMS (agent management system) for builders. Teams supply their LLM API keys; Cubicle is the software development platform built around them.

## What is Cubicle

Cubicle is an agent orchestration platform that runs a software team as a system: agent roles with scoped access and defined handoffs, producing work that flows through tiered human gates.

- **BYOK** — teams bring their own LLM API keys. No token markup, no metered billing.
- **Human gates, agent factory** — agents handle the SDLC mechanics (spec, implementation, testing, reporting); experienced engineers gate what ships.
- **Opinionated by default, customizable to the bone.**
- **IAM / RBAC enforced by spec** — access control is part of the spec, not convention.

## Who it is for

Startups and small orgs with scarce senior talent. The model: a few experienced tech leads act as human gates while the agent team carries the SDLC — multiplying review capacity, not replacing it.

## The core loop

```
repo → spec → implement → test → tiered gate → merged PR
```

Everything else is ornament until this loop runs end-to-end on a real repo.

## Tiered gates

Not every change deserves a human. Gates are tiered by blast radius:

- Low-risk changes pass agent QA and auto-merge.
- Risky changes (auth, migrations, money paths) hit a human gate.

RBAC makes the tiers enforceable. Gate throughput — not code generation — is the bottleneck; the platform is designed around keeping gates cheap and trustworthy.

## Roles

Closer to the codebase: less access, less reasoning, more determinism.

| Role                 | Focus                         | Build priority |
| -------------------- | ----------------------------- | -------------- |
| project-manager      | specs; bad specs waste PRs    | high           |
| senior-developer     | pre-review; keeps gates cheap | high           |
| developer            | implementation                | high           |
| qa-engineer          | test generation + execution   | high           |
| integration-engineer | merges, conflicts, pipelines  | medium         |
| infra-engineer       | onboarding, environments      | medium         |
| technical-architect  | system design oversight       | later          |
| project-owner        | priorities, acceptance        | later          |
| scrum-master         | reporting over git            | last           |

Further sub-divisions (frontend-developer, android-developer, etc.) are planned.

## Build order

1. GitHub App + pipeline: spec → implement → test → tiered gates → PR
2. Dashboard v1: pipeline status, spend per agent, gate queue
3. Depth toggle / founder view: reporting verbosity for non-technical observers

## Status

Building. Core loop in progress — issue fetch shipped behind gated CI; spec, implement, test, and ship stages are next. The living plan is `PLAN.md`; operational procedures are `RUNBOOK.md`.
