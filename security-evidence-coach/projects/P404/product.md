# Cedar rendering SDK

Cedar turns a caller's text into a message for a native renderer. The API contract
requires an immutable UTF-8 byte snapshot and a length in bytes derived from the
same snapshot. The native call is synchronous and does not retain the buffer.
These supplied native-interface promises are assumed for this exercise, not proven
about an external library.

The default desktop adapter is supplied. The mobile factory uses a separate adapter
whose implementation and selection record were not retained. The designated review
scope includes desktop and mobile. Public metadata contains a display title but
never raw document text. The view returns metadata only; rendering is a separate
operation with its own representation contract.

This package is a source/design assessment. It does not include a native binary,
a running product, user data, or an invitation to infer memory corruption from the
mere presence of a native boundary.
