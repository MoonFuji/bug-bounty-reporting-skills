# Delta queued adjustments

Delta accepts logical adjustments within a workspace and processes delivery attempts
asynchronously. A receipt means accepted for processing, not committed. Each pair
(workspace_id, operation_id) may produce at most one committed adjustment. Delivery
attempt IDs and globally unique effect IDs are separate identities.

The same operation_id in different workspaces denotes different logical work.
The reporting projection counts committed effects, not attempts. Compensation, if
performed, is a separate journal event and does not erase earlier history.

This package concerns the complete retained window W4 at revision delta-8. The
journal supplies all committed effects and compensation events for that window.
It does not retain worker interleavings, database statements, or transaction-isolation
settings. Worker retries are allowed; their causes are not established by receipts.
