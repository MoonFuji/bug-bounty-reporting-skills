# Open-ended system assessment projects

These original fictional miniature projects begin with a system, not a suspected
bug. Reconstruct responsibilities, derive a small set of security questions, and
explain what the supplied material establishes. A project may contain an adequately
enforced design, a contract inconsistency, missing evidence, or a mixture.

The materials include product contracts, active or partially retained composition,
pure Python reference components, and finite observation records. They are not
network services, vulnerable targets, or third-party reproduction kits. Their
source can be read without executing it. The exporter never executes project code.

## Learner use

From the skill directory:

```bash
python scripts/assessment_projects.py list
python scripts/assessment_projects.py export --project P101 --output /tmp/coach-P101
```

Give the learner only the export and the selected instruction condition. The
export has one generic brief, allowlisted project files, and SHA-256 identities.
It omits instructor maps, expected themes, and grading guidance. Listing a project
ID does not disclose its conclusion. Filenames are descriptive of components, not
labels such as vulnerable or fixed.

Start without a hypothesis. A useful response explains the system, identifies
material questions with locators, resolves the questions the evidence supports,
and preserves missing dependencies. Neither a finding nor a particular number of
questions is required. Do not declare the whole system safe from a finite review.

## Instructors and maintainers

The [evaluation protocol](../evals/projects/README.md), instructor maps, and worked
walkthrough are public teaching answers. Keep them outside learner access during
an independent attempt. After feedback, later attempts are learning/transfer work,
not held-out evidence. The four projects are not a broad capability benchmark.

The package validator checks artifact links, schemas, and learner/evaluator
separation. It cannot establish that a model chose good questions or understood
a mechanism. Use the human rubric; do not turn filename overlap into expertise.
