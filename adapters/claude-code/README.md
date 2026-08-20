# Claude Code adapter

The repository includes `.claude/agents/*.md` wrappers. When the repository is the active project, Claude Code can discover these as project subagents.

For global installation, copy the wrappers and keep the repository available at a stable path so each wrapper can read its canonical contract:

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/*.md ~/.claude/agents/
```

The wrappers intentionally contain only runtime frontmatter and a pointer to `agents/<name>.md`. The canonical Markdown file remains the source of truth.

Fresh-context roles:

```text
independent-triage-reviewer
final-package-auditor
```

Do not resume the author's context for those roles. Do not grant the reviewer permission to edit `report.md` or the package auditor permission to edit submission artifacts.
