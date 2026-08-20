# Codex adapter

Codex reads the repository-level `AGENTS.md` for the orchestration contract. Use the canonical file from `agents/` as the delegated agent's developer/system prompt.

Recommended delegation payload:

```text
Role contract: agents/<agent-name>.md
Manifest entry: agents/manifest.json#<agent-name>
Task handoff: handoffs/<id>.json
Workspace: <report workspace>
Return only the artifacts owned by this role.
```

For roles with `fresh_context: required`, create a separate isolated task and do not include the author's conversational analysis. Provide only the files listed by the handoff.

To export prompts for an external Codex runner:

```bash
python scripts/export_agent_bundle.py --format plain-dir --output build/codex-agents
```

Codex should not infer permission to submit, disclose, email, or modify target source from these reporting roles.
