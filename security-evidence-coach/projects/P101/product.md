# Atlas shared document workspace

Atlas lets authenticated people read and export shared document summaries. The
record's owner may perform either action. A person from any workspace may also
perform an action explicitly granted to that person on that record. A workspace
label is not, by itself, a share grant. Shares for READ and EXPORT are independent.

READ and EXPORT return the same approved projection: record_id and title.
Internal notes are never part of that projection, including for owners. This
package covers the two public operations at revision atlas-17 and the retained
finite decisions. It makes no claim about future integrations or other products.

The authenticated session provides the principal. The selected permission adapter
receives the resolved record and grants from the trusted store. No background
service acts for a requestor in this version. The service account stores data but
is not substituted for the session principal in a permission decision.
