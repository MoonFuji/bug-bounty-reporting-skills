# Beacon package promotion

Beacon builds packages and records their promotion to a named audience. A valid
build statement identifies an artifact and an authenticated builder. Production
promotion additionally requires a release approver for the same digest and the
production audience. Staging permits the build role under its separate policy.

Signature verification and promotion authorization are separate services. The
supplied records settle verification for one signed build statement. They do not
supply cryptographic source or ask the reviewer to evaluate an algorithm.

At revision beacon-12 the promotion adapter is selected by deployment configuration.
The package contains two policy configurations and the policy consumer. The retained
release record does not include the selected deployment policy or an approval
ledger. Record labels are not substitutes for those artifacts.
