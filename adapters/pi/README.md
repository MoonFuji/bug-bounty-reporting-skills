# Pi agent-harness adapter

Register each `agents/<name>.md` file as an agent type. Load `agents/manifest.json` to configure:

- tool categories;
- read/write artifact scope;
- sandbox mode;
- fresh-context policy;
- terminal statuses;
- certification permissions.

A generic registration loop is:

```text
for agent in manifest.agents:
    prompt = read(agent.file)
    register(name=agent.name,
             prompt=prompt,
             tools=agent.tools,
             sandbox=agent.sandbox,
             fresh_context=agent.fresh_context)
```

The exact Pi registration API may vary by installation; the canonical prompts and manifest remain stable.

Recommended exported bundle:

```bash
python scripts/export_agent_bundle.py --format json --output build/pi-agents.json
```

Enforce a new isolated session for `independent-triage-reviewer` and `final-package-auditor`. The parent orchestrator must not rewrite their verdict artifacts.
