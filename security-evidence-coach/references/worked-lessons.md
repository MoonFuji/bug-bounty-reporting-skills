# Twelve contrastive worked lessons

These are original fictional examples, not real incidents or reproduction guides.
Read a lesson to learn the distinction. For an unaided practice attempt, use only
an exported case packet, not this file or the evaluator's answer key.

Each conclusion is about an exact proposition. SUPPORTED does not always mean a
vulnerability: a proposition can assert that a protection applies. CONTRADICTED
does not mean the whole system is safe. INCONCLUSIVE is neither conclusion.

## 1. Authentication versus permission

**Tempting inference:** a request succeeded while signed in and failed after
logout, so the access was correctly authorized.

**Case A:** the contract makes records owner-confidential unless shared. The
operation-specific snapshot says R belongs to B and no grant applies to A. A is
authenticated. The proposition "A was authorized" is contradicted by the contract
and grant state; the authentication event does not override them.

**Case B:** the same contract and request, but the snapshot includes an active
read grant from B to A for R. The proposition is supported. A tenant or ownership
difference is not sufficient evidence that access is forbidden.

**Transfer question:** what changes if the grant snapshot is missing? Permission
becomes unresolved; do not assume either a grant or its absence.

## 2. Local code versus delegated authority

**Tempting inference:** no check in the handler means no check on the operation.

**Case A:** complete supplied bindings require policy P before every invocation,
and P authorizes the same resolved object, caller, and action. The allegation
that the operation lacked an applicable decision is contradicted.

**Case B:** only the handler excerpt is supplied; bindings and policy are absent.
The same allegation is inconclusive. "The framework probably handles it" is not
counterevidence, just as an omitted binding is not proof of an omitted defense.

**Transfer question:** is a check on a different object sufficient? No; its
applicability to the protected effect still needs to be established.

## 3. Missing observation versus observed absence

**Tempting inference:** zero captured events proves no event occurred.

**Case A:** the instrument was inactive. The event-absence claim is inconclusive.
The empty capture is compatible with both event occurrence and event absence.

**Case B:** a finite simulator records every emission synchronously, the instrument
control succeeded, and a gap-free stream covers exactly the operation interval.
The same bounded event-absence claim is supported within that model.

**Transfer question:** does Case B prove that a production service never emits an
event? No. Instrument completeness and the finite model do not generalize beyond
the specified environment and interval.

## 4. Observable difference versus causal disclosure

**Tempting inference:** different bodies prove a confidential state was revealed.

**Case A:** the requests differ in state, locale, and request identifier. A body
difference exists, but those facts do not identify its cause. The claim that it
discloses the state bit is inconclusive.

**Case B:** the complete finite serializer contract uses only a constant message
and an independently assigned request ID; bodies differ only in that ID. The
body-disclosure allegation is contradicted for that model and channel.

**Transfer question:** are timing and status also cleared? No. A conclusion about
one observation channel is not automatically a conclusion about another.

## 5. Preliminary state versus committed transition

**Tempting inference:** two workers accepted the same adjustment, so both effects
committed.

**Case A:** the contract says acceptance precedes deduplication; the final journal
is absent. The duplicate-commit proposition is inconclusive.

**Case B:** an authoritative final journal records two distinct committed balance
changes for the same logical adjustment. An integrity record excludes duplicate
log delivery and rollback. The duplicate-commit proposition is supported.

**Transfer question:** why does the integrity record matter? Two identical log
lines could describe one effect. The conclusion depends on effect identity, not
merely the number of printed messages.

## 6. Canonical identity versus opaque identifiers

**Tempting inference:** similar-looking strings always identify the same object,
or normalization is always safer.

**Case A:** the namespace explicitly defines Maple and maple as equivalent and
both authorization and lookup use that mapping. Same-object identity is supported.

**Case B:** identifiers are explicitly opaque and case-sensitive; those labels
identify distinct objects. Same-object identity is contradicted. Lowercasing here
would change the contract rather than enforce it.

**Transfer question:** what matters more than the existence of a normalizer?
Whether decision and effect use the intended identity relation and namespace.

## 7. Revision fidelity versus deployment provenance

**Tempting inference:** a run uses production's source revision, so it occurred
in the managed production service.

**Case A:** an operation-specific owner attestation and inventory bind run F and
revision Z to the designated managed deployment. The provenance claim is supported.

**Case B:** the attestation places the same revision's run on a distinct local
development runner. The provenance claim is contradicted.

**Transfer question:** does Case B disprove the behavior in production? No. It
only identifies where this run occurred. Neither location alone establishes an
additional security consequence.

## 8. Powerful action versus increased privilege

**Tempting inference:** a powerful operation succeeded, therefore privilege grew.

**Case A:** the starting principal already possessed the exact permission; the
operation used it and the final authority was unchanged. Escalation is contradicted.

**Case B:** only completion is recorded; starting permissions and effective identity
are unavailable. Escalation is inconclusive, not established by the operation name.

**Transfer question:** which comparison is essential? Starting effective authority
versus resulting effective authority across the claimed boundary, not the dramatic
name of an action.

## 9. Public search versus complete duplicate knowledge

**Tempting inference:** no public match means no earlier report exists.

**Case A:** a public search completed, but the private report pool was inaccessible.
The proposition "no prior report covers this cause" is inconclusive.

**Case B:** an earlier report is supplied with the same boundary, cause, invariant,
affected revision, and effect; only title and demonstration wording differ. The
absence proposition is contradicted.

**Transfer question:** does a different title establish novelty? No. Conversely,
the same title alone is not sufficient to establish a duplicate either.

## 10. Technical impact versus program treatment

**Tempting inference:** a reduced reward ceiling reduces the technical severity.

**Case A:** technical effect and preconditions are unchanged; only the monetary
rule changed. The claimed causal reduction in technical impact is contradicted.

**Case B:** a report originally claimed host-wide impact, but its evidence covers
only one isolated process-level effect. The proposition that the evidence is
narrower than the report is supported. Here narrowing follows evidence, not price.

**Transfer question:** does missing host-boundary evidence prove a host-wide effect
is impossible? No. It prevents treating that extension as demonstrated.

## 11. Asynchronous acknowledgment versus completion

**Tempting inference:** accepted means completed.

**Case A:** the packet includes a correlated authoritative durable record for the
named operation. Commitment is supported by that record, not the initial ack.

**Case B:** only an acknowledgment is available, and the contract allows later
rejection without effect. Commitment is inconclusive. Final rejection is also
unestablished.

**Transfer question:** can an unrelated completion event fill the gap? No. The
authoritative record must describe the operation whose outcome is claimed.

## 12. Finite coverage versus a clean system

**Tempting inference:** a closed checklist proves the whole product is secure.

**Case A:** the agreed finite matrix contains A, B, C, and D; accessible completed
assessments exist for each. Coverage of this matrix is supported, not whole-product
security or completeness of the original matrix.

**Case B:** D has no accessible assessment record; the author merely recalls
finishing. Complete assessment is inconclusive. The missing record also does not
prove that D was never assessed.

**Transfer question:** how should a resumed review start? From the existing records
and the unresolved D dependency, not from the old author's "done" label.

## Using the lessons responsibly

These packets deliberately state some facts authoritatively so their expected
answers can be checked. Real reviews must establish provenance and applicability;
they cannot assume that every supplied summary is complete or truthful. Evaluate
transfer with new owner-controlled material, not just these same stories reworded.
