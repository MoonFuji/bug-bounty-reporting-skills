# Research integration brief

## Decision

The completed mobile research has been incorporated into `mobile-app-hunter`.
The report proposed that name, and the branch adopts it before the skill's first
merge, release, or installation. The earlier `mobile-app-security-assessment`
name was only an uninstalled working name, so no compatibility alias is needed.
The report's useful contribution remains architecture-aware judgment rather than
a larger mandatory workflow.

Research snapshot: 2026-09-09. Integration: 2026-09-10. Source status and primary
URLs are in [sources](sources.md) and [source-index.json](source-index.json).
The integration read the completed report and its citation metadata; it did not
perform a second external retrieval or app/runtime evaluation.

## Adopted findings

| Research finding | Implemented location | Important limit |
|---|---|---|
| Start before a suspected bug exists | Existing Assess path plus [assessment design](assessment-design.md) | Designated code/artifacts; no autonomous target acquisition |
| Build composition is security-relevant | [Research lessons](research-integration.md#release-composition) | A dependency name is not evidence of an affected selected path |
| Platform behavior needs selectors | [Applicability](research-integration.md#platform-applicability) | OS, target SDK, build and library versions are not interchangeable |
| Strong primitives do not prove composition | [iOS and framework lessons](research-integration.md#ios-authority-and-data) | Signing, storage and integrity are separate from business permission |
| MASVS/MASTG backstop architecture work | [Coverage map](research-integration.md#standards-as-a-coverage-backstop) | Categories and a named release, not invented test IDs |
| Use historical reports as mechanism lessons | [Documented examples](research-integration.md#documented-case-lessons) | No payloads, current-vendor claims or assumed fixed-version coverage |
| Test selection and transfer, not only verdicts | [New transfer tasks](../evals/research-transfer.md) | Human rubric; public teaching tasks, not held-out benchmarks |
| Keep core short and resources directly reachable | [Design note](../evals/skill-design.md) | No Anthropic certification or measured model gain |

## What this does not claim

This update does not upgrade every old background link to verified. The report
itself identified incomplete retrieval for some Apple API documentation. Two
advisories mentioned as leads do not become detailed historical cases. Exact
platform defaults absent from the report still need applicable primary sources.

The MASTG v2.0.0 announcement is the research's identified baseline. This is not a
claim that it is always the latest, or that this package implements every test.
No change to a bounty program's eligibility, scope or rewards is inferred.

The research also proposed a larger tool suite and a more extensive hunting
loop. This integration keeps human-directed architecture/source assessment,
controlled defensive evidence interpretation, and ordinary continuation notes.
It does not add exploitation, service scanning, protection bypasses, payload
construction, or automatic finding submission. No new app-inspection binaries
or framework dependencies are required.

## Evaluation next, not more pages by default

Run a baseline and skill-assisted assessment on the same designated project,
with matched artifact revision, tools, budget and output task. Evaluate relevant
question selection, correct authority/composition, conclusions and justified
unknowns. Repeat runs and include secure and incomplete-evidence variants.
Score substantive arguments, not vocabulary, tool volume or number of findings.

The source-index and CI tests validate the package. Only actual independent
model runs can establish that this curriculum improves performance. None have
been performed by this integration.
