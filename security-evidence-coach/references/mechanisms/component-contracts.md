# Libraries, SDKs, and caller contracts

## A component guarantee has preconditions

A library can correctly guarantee G when its caller provides P. A product using the
library must establish P before relying on G. If the caller never establishes P,
blaming the library by default can misidentify the responsibility. If the library
promises G without P, inventing P after observing a discrepancy is equally unsound.

Write the assumption and guarantee separately. Use the designated API contract,
implementation version, and active call site. Names such as sanitize, verify, or
safe do not define an assurance. A successful return may mean parsed, accepted,
queued, or committed; read which meaning the interface promises.

## Selection and wrappers matter

Dependency injection, platform adapters, optional backends, generated clients, and
configuration can select different implementations. A correct source listing is not
enough unless it is connected to the operation. Conversely, an intentionally thin
wrapper need not repeat a guarantee already enforced by an applicable shared layer.

Error handling is part of composition. An exception, timeout, partial result, or
optional value must be interpreted according to its contract. A missing result does
not automatically mean deny, rollback, or success. Record what the actual caller does
with it, without asserting that an unused example is production behavior.

## Contrast

A fictional directory SDK guarantees object filtering when given an already resolved
permission context. Adapter C obtains that context from the selected permission
service; adapter D's documentation delegates it to the caller. The same SDK function
may be correct in both contexts, while the integrator has different obligations.
If the runtime adapter is not supplied, neither composition is established.

Another example uses a method returning an acceptance receipt. A wrapper labels that
receipt completed, but the product contract requires a committed record for completion.
The question is the meaning carried across the interface, not whether the word success
appears in a log. A real consequence remains a separate claim needing evidence.

## Meaningful local tests

Tests should exercise the relevant contract with independently specified expectations.
A fake permission service can test a wrapper's reaction to allow and deny results; it
cannot establish how the real service decides. A mock transport may test serialization
but not the actual remote consumer. Record these boundaries instead of treating all
passing integration-looking tests as equivalent.

## Transfer question

Move a required precondition from the caller into a new library version. Which
responsibility changes, and which historical result remains tied to the old version?
Pin the revision instead of assuming a current contract describes all past releases.
