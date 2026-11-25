# Agent Guardrails Demo

A five-minute, browser-only demo of a human-checkpoint workflow for AI coding agents. Jira is the intake, GitHub is the governed change surface, and a scripted stand-in plays the agent.

## What the demo proves

1. A Jira ticket is the work request.
2. The agent proposes a plan; a human approves it before any code changes.
3. The agent works on its own branch and opens a pull request. It never pushes to `main` and never deploys.
4. GitHub Actions runs tests and a dependency vulnerability scan on the pull request.
5. A separate human account reviews and merges.
6. Branch protection rejects direct pushes to `main`.

This demonstrates process controls. It is not a demonstration of any specific vendor's agent product.

## Account roles

| Role | Account | Can do |
|---|---|---|
| Agent (bot) | `hbwebadmin-png` | Owns the repo, creates branches, opens PRs |
| Human reviewer | `sfc-gh-hbarile` | Reviews and approves PRs (listed in `CODEOWNERS`) |
| Intake | Jira Cloud site | Holds the ticket and the plan-approval signal |

No GitHub, Jira, or agent credentials belong in this repository. Use GitHub Actions secrets or a local secret store.

## Repository layout

| Path | What it is |
|---|---|
| `app/pricing.py` | Tiny sample application the agent maintains |
| `tests/test_pricing.py` | Unit tests that CI runs on every PR |
| `requirements.txt` | Pinned dependencies; the demo ticket upgrades one of them |
| `agent.py` | Scripted stand-in agent: prints a plan, stops until approved |
| `personas/` | Planner, Implementer, and Reviewer instructions |
| `.github/workflows/demo-agent.yml` | CI: approval gate, tests, dependency scan |
| `CODEOWNERS` | Names the human who must review changes |

## Five-minute run

1. Open the Jira ticket: `Upgrade the vulnerable dependency and add a regression test`.
2. The agent posts its plan as a Jira comment.
3. The presenter adds the `plan-approved` label in Jira.
4. In GitHub, run **Actions > Web Agent Demo > Run workflow** with the ticket key and approval box checked.
5. The agent pushes branch `agent/<ticket>` and opens a PR.
6. Show the CI checks go green, then approve the PR as the reviewer.
7. Show that `main` is protected and a direct push is rejected. Close with: "The agent proposes; your engineers decide."

The manual **Run workflow** button is used instead of Jira Automation, which avoids storing a GitHub credential inside a Jira rule.

## Scope boundary

The demo does not touch production systems or data.
