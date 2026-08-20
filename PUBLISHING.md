# Publishing

The intended public repository is:

```text
MoonFuji/bug-bounty-reporting-skills
```

## GitHub CLI

From this directory:

```bash
gh repo create MoonFuji/bug-bounty-reporting-skills \
  --public \
  --description "Composable Agent Skills for writing, hardening, reviewing, and adapting vulnerability reports" \
  --source . \
  --remote origin \
  --push
```

## Existing empty repository

```bash
git remote add origin git@github.com:MoonFuji/bug-bounty-reporting-skills.git
git push -u origin main
```

Do not initialize the GitHub repository with a README, license, or `.gitignore`; those files already exist here.
