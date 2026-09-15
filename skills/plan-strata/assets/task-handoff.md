# Worker handoff — {{task_key}} / {{attempt}}

Optional fallback: an existing host assignment and bound task card can supply this
contract directly. Follow {{skill}}; retain the dispatched assignment revision.

## Assignment

- Source access and workspace/location or creation instructions: {{project}}
- Worker, or allocating coordinator and pickup procedure: {{worker}}
- Plan binding: {{plan}}
- Retrievable source/input baseline, including relevant dirty inputs: {{baseline}}
- Manager, designated progress writer, and record location: {{manager}}
- Relevant context not already recovered: {{context}}

{{objective}}

- Inputs, accepted dependency versions, and release conditions: {{dependencies}}
- Allowed writes and report/evidence locations: {{write_scope}}
- Shared interfaces/resources and other constraints: {{constraints}}
- Acceptance and verification: {{acceptance}}
- Applicable user/host limits, stop conditions, and external permissions: {{budget}}

## Return

Return via {{report}}: task/attempt, delivery revision and binding; changed paths
and retrievable versions; actual checks/results/exit codes; limitations and next
recommendation. Include usage where budgeted and any unfinished job handles/outputs.
This completes the Worker delivery for review, not task acceptance. Continue
authorized repairs under the same assignment with new delivery/report versions;
preserve earlier returns. Only the designated writer updates progress.
