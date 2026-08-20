# Harness adapters

The canonical source of truth is `agents/manifest.json` plus `agents/*.md`. Runtime adapters should point to those files rather than maintain independent prompt copies.

| Harness | Integration |
|---|---|
| Claude Code | Ready-to-use wrappers in `.claude/agents/`. |
| Codex | Repository-level `AGENTS.md` plus canonical Markdown prompts for delegated tasks. |
| Pi | Register canonical Markdown prompts as agent types and enforce manifest tool/freshness scopes. |
| Other harnesses | Run `scripts/export_agent_bundle.py` to produce JSON, JSONL, or a plain prompt directory. |

A harness adapter is correct only when it preserves:

- role mission and prohibitions;
- input/output artifact ownership;
- fresh-context requirements;
- the exclusive report-certification and package-certification roles;
- claim-preserving handoffs.
