# Changelog

## Unreleased — portable reporting-agent layer

- Add 13 harness-neutral agent contracts: seven core pipeline roles and six optional specialists.
- Add a machine-readable manifest with tool, sandbox, freshness, read/write, and certification scopes.
- Add direct Claude Code subagent wrappers, a Codex `AGENTS.md` contract, Pi integration guidance, and JSON/JSONL/plain prompt export.
- Enforce separation of duties: writers and hardeners may mutate reports, only the fresh triage reviewer may issue `READY`, and only the fresh package auditor may issue `PACKAGE_READY`.
- Add persisted pipeline-state and handoff contracts.
- Add deterministic validation for role definitions, runtime wrappers, certification boundaries, artifact ownership, fresh-context handoffs, and portable exports.
- Extend CI and repository validation to cover the complete agent layer.

## v0.1.0 — initial reporting pipeline

- Add four composable Agent Skills: write, harden, review, and adapt.
- Add a canonical report-input bundle and manifest.
- Add an Invariant-First candidate converter that refuses non-final candidates.
- Add deterministic Markdown and review validators with regression tests.
- Add realistic eval prompts for every skill.
- Add repository validation and GitHub Actions.
