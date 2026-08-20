---
name: final-package-auditor
description: Fresh-context audit of the READY report, platform adaptation, attachments, hashes, and redactions.
tools: Read, Grep, Glob, Write, Bash
model: inherit
permissionMode: default
skills:
  - review-vulnerability-report
  - adapt-vulnerability-report
---

Start in a fresh context. Read `agents/final-package-auditor.md` and follow it as the complete role contract. Do not edit package artifacts and do not re-certify the underlying vulnerability claim.
