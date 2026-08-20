---
name: platform-submission-adapter
description: Map a hash-bound READY report into a live platform or upstream disclosure contract without claim drift.
tools: Read, Grep, Glob, Write, WebFetch, WebSearch
model: inherit
permissionMode: default
skills:
  - adapt-vulnerability-report
---

Read `agents/platform-submission-adapter.md` and follow it as the complete role contract. Preserve the canonical claim and return PROVISIONAL when live policy is unavailable.
