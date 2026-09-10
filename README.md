# Bug Bounty Reporting Skills

A portable Agent Skills collection for turning validated vulnerability evidence into clear, reproducible, triager-ready disclosures.

The reporting pipeline deliberately starts **after discovery**. It does not decide whether a suspicious behavior is a vulnerability and it does not lower proof, scope, ownership, or novelty gates. Give it a finalized evidence bundle or a validated candidate from an upstream hunting workflow. The optional Security Evidence Coach supports architecture-first assessment before a suspected bug exists, as well as evidence judgment; neither a practice result nor an assessment note is validated reporting input.

## Included skills

| Skill | Job |
|---|---|
| [`write-vulnerability-report`](write-vulnerability-report/) | Turn validated evidence into one self-contained canonical report without inventing impact. |
| [`harden-vulnerability-report`](harden-vulnerability-report/) | Improve radius analysis, reproduction reliability, severity accuracy, and remediation while preserving the evidence boundary. |
| [`review-vulnerability-report`](review-vulnerability-report/) | Run a fresh-context, triager-minded final review and issue `READY`, `BLOCKED`, or `PROVISIONAL`. |
| [`adapt-vulnerability-report`](adapt-vulnerability-report/) | Adapt a canonical final report to a live platform or upstream disclosure contract without changing its claims. |
| [`security-evidence-coach`](security-evidence-coach/) | Investigate designated software from its architecture, derive relevant assessment questions, explain security mechanisms, and review evidence without certifying expertise or report readiness. |
| [`mobile-app-security-assessment`](mobile-app-security-assessment/) | Assess designated Android APK/split/AAB or iOS IPA/source material from app architecture, platform authority, and evidence; includes offline metadata intake and fictional practice. |

## Recommended reporting pipeline

```text
validated candidate / evidence bundle
                |
    write-vulnerability-report
                |
   harden-vulnerability-report
                |
   review-vulnerability-report
                |
    READY canonical report
                |
    adapt-vulnerability-report
                |
 platform-ready submission package
```

The canonical report is the source of truth. Platform adaptation may reorder, shorten, or split fields, but it must not add impact, broaden scope, change severity, or omit load-bearing limitations.

## Mobile assessment companion

[`mobile-app-security-assessment/SKILL.md`](mobile-app-security-assessment/SKILL.md) starts from a designated app without requiring a suspected bug. Its Android-first path covers package/install identity, components and delegation, storage/key lifetimes, links/WebViews, network and backend authority, and native/framework boundaries. A distinct iOS path covers signing/entitlements, Keychain, groups/extensions, local authentication, and device-versus-simulator evidence. Detailed references load only when relevant; ordinary work requires no new ledger or quiz.

```text
Use $mobile-app-security-assessment to assess this designated mobile app.
No suspected vulnerability is supplied. Explain its security responsibilities,
prioritize material questions, cite applicable build/runtime evidence,
and preserve unresolved dependencies without inventing impact.
```

The [research brief](mobile-app-security-assessment/references/research-brief.md) now applies the completed September 9, 2026 Deep Research report, which attributes discovery to Exa and framework/authoring retrieval to Context7. The [research integration chapter](mobile-app-security-assessment/references/research-integration.md) covers platform applicability, generated release composition, web/native trust, iOS data/capabilities, framework adapters and MASVS coverage. The [source register](mobile-app-security-assessment/references/sources.md) distinguishes 17 report-cited sources, three limited-content Apple API pointers and two historical research leads; inherited citations are not fresh independent retrieval in this implementation. Detailed unsupported claims remain unresolved. The [skill design note](mobile-app-security-assessment/evals/skill-design.md) connects the report's Anthropic guidance to a 201-line core, progressive disclosure and baseline evaluations without claiming certification.

Sixteen worked contrasts and eight fictional multi-artifact projects teach app-specific assessment questions and calibrated conclusions. Learner exports exclude instructor maps. The optional inventory reads bounded ZIP metadata without extracting, installing, or executing app contents; it is not a vulnerability scanner or signature verifier. This is human-directed assessment, not autonomous third-party targeting or exploitation.

```bash
python mobile-app-security-assessment/scripts/artifact_inventory.py /path/to/designated.apk
python mobile-app-security-assessment/scripts/mobile_projects.py validate
python mobile-app-security-assessment/scripts/validate_research.py
python mobile-app-security-assessment/scripts/mobile_projects.py export --project M214 --output /tmp/mobile-project
python -m unittest discover -s mobile-app-security-assessment/scripts -p 'test_*.py'
```

The package includes 105 offline software tests: the original 66 plus 39 research-metadata regressions. Three new [paper transfer tasks](mobile-app-security-assessment/evals/research-transfer.md) complement the unchanged eight-project corpus; give learners only the task file, not its separate instructor notes. No Android/iOS runtime, external service, or model was evaluated. The [evaluation guide](mobile-app-security-assessment/evals/README.md) requires human review of architecture, question selection, evidence, and uncertainty; tool success never grants report readiness.

## Architecture-first assessment companion

[`security-evidence-coach/SKILL.md`](security-evidence-coach/SKILL.md) now starts with **Investigate** when given a designated codebase or system without a suspected bug. It reconstructs security responsibilities, derives material questions from the actual architecture, and connects source, active configuration, contracts, and observations. Explain, Review, and Practice remain available. This is human-directed source/design assessment, not autonomous third-party targeting or exploitation.

```text
Use $security-evidence-coach to investigate this designated codebase.
No suspected vulnerability is supplied. Explain its security responsibilities,
choose the material questions, cite active bindings and relevant artifacts,
and distinguish settled facts from unresolved assessment dependencies.
```

The [architecture-first guide](security-evidence-coach/references/architecture-first-assessment.md) explains how questions arise before a claim exists. Eight [mechanism chapters](security-evidence-coach/references/mechanisms/README.md) cover identity and permission; asynchronous state; signed statements; build and delivery; component contracts; process/resource authority; representation/native interfaces; and device updates. Load only the chapters relevant to the uncertainty. Normal assessment needs no quiz, scoring form, or new mandatory ledger.

Four [open-ended multi-file projects](security-evidence-coach/projects/README.md) begin with product behavior, source components, composition, and observations rather than a prewritten hypothesis. They include secure look-alikes, an established finite inconsistency, incomplete evidence, and mixed outcomes. The [human evaluation rubric](security-evidence-coach/evals/projects/README.md) assesses architecture understanding, question selection, grounding, calibration, continuation, and transfer. Instructor material is separate from learner exports.

```bash
python security-evidence-coach/scripts/assessment_projects.py validate
python security-evidence-coach/scripts/assessment_projects.py list
python security-evidence-coach/scripts/assessment_projects.py export --project P101 --output /tmp/coach-project
python security-evidence-coach/scripts/test_assessment_projects.py
```

### Existing evidence practice is preserved

The coach retains twenty worked lesson families, 48 fictional evidence packets across foundation and advanced tracks, twelve qualitative evaluation prompts, six staged revision drills, separate evaluator answer keys, and the original exporter/scorer. Two defensive specification models and an evidence-arithmetic model make bounded concepts executable. These train judgments after a question exists; the new project track complements them without changing their suite IDs or packet bytes.

The [advanced lessons](security-evidence-coach/references/advanced-worked-lessons.md) connect source bindings, policy composition, revocation order, committed effects, stratified measurements, provenance, remediation evidence, and relational observations.

```bash
python security-evidence-coach/scripts/practice.py validate
python security-evidence-coach/scripts/practice.py export --output /tmp/security-practice-inputs
python security-evidence-coach/scripts/test_practice.py
python security-evidence-coach/labs/test_models.py
python security-evidence-coach/scripts/practice.py validate --suite advanced
python security-evidence-coach/scripts/practice.py export --suite advanced --output /tmp/security-advanced-inputs
python security-evidence-coach/scripts/test_advanced.py
python security-evidence-coach/labs/test_evidence_math.py
```

Give assessed agents only the export and the chosen instruction condition, not answer keys or instructor maps. These public projects are teaching material, not a private capability benchmark. The tools do not invoke models, execute project text, or grade the truth of prose. Human review is required. No measured improvement on any model is claimed.

Live web research was unavailable during authoring. The [source register](security-evidence-coach/references/sources.md) labels external reading links as unverified; all new projects are original and synthetic, not copied bounty reports.

## Installation

```bash
npx skills add MoonFuji/bug-bounty-reporting-skills --list
npx skills add MoonFuji/bug-bounty-reporting-skills
```

Each skill is self-contained and can also be copied individually into an Agent Skills directory.

## Canonical input

`write-vulnerability-report/assets/report-input.template.json` defines the portable evidence bundle. The writer also accepts a validated `candidate.json` from the Invariant-First Bug Bounty skill; use:

```bash
python write-vulnerability-report/scripts/from_invariant_candidate.py \
  candidate.json \
  report-input.json
```

The converter refuses non-reportable, self-certified, or review-owed candidates. The coach does not bypass this contract.

## Mechanical checks

```bash
python -m compileall -q .
python scripts/validate_repo.py
python write-vulnerability-report/scripts/test_validate_report.py
python review-vulnerability-report/scripts/test_validate_review.py
```

Validate a finished report:

```bash
python write-vulnerability-report/scripts/validate_report.py \
  report.md \
  --manifest report-manifest.json
```

Validate an independent review:

```bash
python review-vulnerability-report/scripts/validate_review.py \
  review.json \
  --report report.md
```

## Design rules

- **Evidence before prose.** A polished sentence cannot repair an unproven claim.
- **One canonical claim.** Every title, summary, severity statement, reproduction step, and platform adaptation must describe the same demonstrated capability.
- **Limitations remain visible.** A load-bearing limitation blocks readiness; an ordinary limitation constrains scope or severity and stays in the report.
- **No process leakage.** Reports do not expose internal gate names, candidate field names, model deliberation, or agent metadata.
- **Stable references.** Repository links point to immutable revisions, not moving branches.
- **Fresh final review.** The author may self-edit, but final certification is performed by a separate context or a human on the final report.

## Scope and safety

Use these skills only for authorized research and coordinated disclosure. Never include live credentials, third-party personal data, private program material, or undisclosed vulnerability details in public examples, issues, or pull requests.

## License

MIT. See [LICENSE](LICENSE).
