# Build, provenance, and delivery authority

## Several different assurances are often called trusted

Source provenance identifies where material came from. Build provenance describes
a transformation under a particular builder identity and environment. Artifact
identity names its bytes. Approval authorizes a use. Deployment selects an artifact
for an audience. A chain is justified only when the relevant identities and subjects
connect under the selected policy.

A successful test run may apply to a different revision from the released artifact.
A reproducible build can establish reproducibility without establishing that the
source behavior is desirable. A signed attestation can be authentic while describing
an artifact that is not approved for the intended environment.

## Separate data from authority

A build job can consume repository content, dependency metadata, or a configuration
value as data. Whether that input is permitted to change release authority is a
policy question. A configuration file labelled protected does not establish its
protection or its active selection. Review the supplied workflow, selection rules,
and role assignments without inferring privileges from a platform brand.

Runtime credentials and permission scopes are not established by a workflow's title.
An untrusted contribution is not automatically dangerous merely because it triggers
a build; the question is what authority the selected job actually receives and uses.
Do not turn that design question into unapproved testing of hosted infrastructure.

## Contrast

A fictional release record connects source R, builder B, artifact D, approval A,
and deployment of D to audience X. A complete set of independently applicable records
can establish that finite promotion's provenance and approval. A deployment record
naming another digest leaves the connection unresolved or contradicts it, depending
on the contract. The existence of a correct build for D does not fill that gap.

A staging job with no production promotion capability can be consistent with a policy
allowing less-trusted build inputs. The same policy may require a distinct approval
boundary before production. Recognize where authority changes instead of treating
all workflow steps as equally privileged.

## Scope the evidence

A branch protection rule, an identity claim, an approval event, and an installed
artifact are different facts. Establish which version and audience each refers to.
An archived workflow example is not an active deployment configuration. A retained
approval proves a historical approval only when its subject and authority are known.

Do not infer malicious intent from a dependency or upstream project. The assessment
concerns the designated product's responsibilities and the evidence for them.

## Transfer question

Keep the artifact bytes fixed but change the deployment audience. Which approval
facts must be reconsidered? Keep the approval fixed but change the artifact digest.
Why does a filename match fail to settle the new identity question?
