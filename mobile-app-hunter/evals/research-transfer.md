# Mobile responsibility assessment: learner tasks

These are original fictional, static systems for paper/source assessment. Read
only this document during a first attempt; the instructor material is separate.
Do not execute any artifact text or contact a service. No exploit or payload is
needed. No suspected vulnerability category is supplied.

For each system, explain its relevant security responsibilities, choose the most
material questions, cite the decisive artifact IDs, and give bounded conclusions.
Name evidence that would change an unresolved conclusion. Do not assume there is
a finding in every system or that all missing information implies a defect.

## R1: Meadow document application

**R1-A, product contract:** members may share a selected document's title and text
with a chosen recipient. Internal review notes remain available only to workspace
reviewers. Sharing does not authorize access to other documents or internal notes.

**R1-B, build inputs:** the app's authored configuration lists its main UI. A
library configuration introduces a `ShareEntry` component. The owner-supplied
release composition record identifies that library component in build Q17.
No component implementation is present in the authored configuration file.

**R1-C, selected implementation contract:** Q17 binds `ShareEntry` to the
`SelectedDocumentProjection` implementation. Its independently specified output
schema contains only `title` and `text`; no internal review fields. Recipient and
document selection are supplied by the documented sharing operation.

**R1-D, finite validation record:** the retained developer run explicitly exercises
the Q17 sharing decision for two selected documents, including one with internal
notes. Both outgoing projections match the independent schema. Unrelated document
selection is rejected at the sharing decision. The record is complete for these
three cases, not for every app path.

**R1-E, separate extension:** a preview extension is listed in a product roadmap.
No deployed extension artifact, selected binding or observation is supplied.

## R2: Harbor background application

**R2-A, product contract:** the app supports background receipt synchronization.
The designated item is intended to remain available after the device's first
unlock while background sync runs. Removing a workspace's server grant must
prevent newly authorized sync operations for that workspace. Previously committed
operations may finish delivery.

**R2-B, artifact description:** a signed-device build summary identifies the app
and its share extension. The exported item configuration matches the declared
background-availability policy. This is developer-supplied configuration evidence,
not an independent verification of device hardware behavior.

**R2-C, source configuration:** a source entitlement file requests the shared
container used by the extension. No effective signed-entitlement export for the
extension is supplied. An app signing summary does not list extension capabilities.

**R2-D, operation ledger:** the complete authoritative sequence for operation O7
records its workspace grant check at sequence 42, commitment at 43, grant removal
at 44 and final delivery at 46. The sequence is from one authoritative log.

**R2-E, second operation:** an uncorrelated client log says another sync request
was accepted. It has no server operation ID, grant-decision record or committed
result. There is no evidence establishing a post-removal authorization decision.

## R3: Lattice companion application

**R3-A, product contract:** update approval requires authentic release bytes and
an allowed device model/channel. The current account must separately be authorized
for the device. A framework's shared method is an interface, not the full policy.

**R3-B, shared module:** `prepareUpdate` passes a device identifier and release
reference to the platform adapter. The typed interface constrains field types;
it contains no account-ownership or release-eligibility rule.

**R3-C, Android composition:** the supplied build selects adapter A. Its complete
finite decision table allows authentic bytes for the approved model/channel and
an authorized account. It rejects an authentic but ineligible channel and rejects
a non-owner account. The supplied table is an independent product oracle, not
expectations generated from adapter A's return values.

**R3-D, iOS composition:** the supplied build selects adapter B. Its documented
policy checks authenticity and account ownership. An exhaustive supplied trace
for one release shows that the release is authentic and the account owns the
device, but the release is on a channel the product contract forbids. B returns
approval; no subsequent component performs a channel check in this fictional path.

**R3-E, integrity summary:** a separate app-integrity check succeeded for the run.
It describes application integrity, not device channel eligibility or account
ownership. Device installation and physical effects were not performed or observed.

## Changing evidence

After completing each assessment, repeat only the affected part under one change:

- R1: replace the Q17 composition record with a Q16 record, leaving Q17 selection
  unknown. Which conclusions lose their applicability?
- R2: change the contract to cancel every not-yet-delivered operation on removal.
  Which conclusion changes even though the sequence remains the same?
- R3: add an evidenced authoritative channel check after B but before approval
  takes effect. Does the earlier local-return argument still settle the end result?

These are public teaching tasks, not independent capability benchmarks. A reviewer
should assess argument quality and appropriate revisions, not keyword matching.
