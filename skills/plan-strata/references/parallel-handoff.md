# Optional parallel handoffs

Delegation requires explicit authorization for the iteration/batch; a received
assignment traceable to that batch reuses it. A proposal request does not authorize
dispatch. Use the host's existing tools/adapter within that authority; no extra
opt-in or configuration switch is needed. External posting, paid jobs, pushing,
and merging still need their corresponding permissions. If delegation is unavailable,
use an authorized manual handoff or sequential execution and disclose the limitation.

## Ownership and progress bookkeeping

Keep one allocation authority for all dispatchers. Assign ready tasks from one
plan with available inputs/accepted dependencies, settled shared interfaces, safe
write scopes, and applicable resource limits. Isolate conflicting writes or
serialize them; Git branches in one directory do not isolate files, and worktrees
do not isolate shared services or compute. The skill supplies neither scheduler
nor lock; a stale `planned` row is not a claim.

A host assignment message plus its bound task card can be the complete handoff.
Use an existing adapter's exclusive task/attempt, workspace, and resource allocation
directly; execution need not wait for a progress owner entry. After the host returns
the Agent ID, the designated writer retains the dispatch receipt: assignment/binding,
owner, workspace/output location, and runtime handle. Reconcile it before retry,
further dispatch, or acceptance. Without such an adapter, record allocation before
execution. Ambiguous ownership pauses writes/retry on the affected task.

Retain the dispatched assignment/task-card revision in a recoverable channel.
Use the [worker template](../assets/task-handoff.md) only when a handoff format is
missing, not alongside an already complete assignment.

## Cold-start gate

An executable handoff supplies the objective, binding, retrievable baseline/inputs,
entry conditions, allowed writes, acceptance, applicable limits, and return
destination. Include only relevant context, accessible from the recipient's actual
environment. For Git pickup, identify the repository, a fetchable ref containing
the pinned commit, and any retained dirty/untracked inputs. A moving branch or a
Manager-only local path is not a delivered baseline.

For Issue dispatch, put the task contract in the body; detailed context can link
to fixed, retrievable versions. Verify those references before calling it ready.
Missing publication authority cannot be bypassed by pushing the inputs. A complete
handoff can be unclaimed: identify the allocating coordinator and workspace creation
procedure. An authorized draft can await dependencies: state its missing inputs
and release conditions, then pin actual accepted deliveries before execution.
An upstream Issue closing is not itself dependency acceptance.

Completeness, readiness, and allocation are distinct judgments, not new protocol
states. The validator does not parse or enforce this handoff contract.

## Worker: execute the bound assignment

Recover the assignment and only missing/stale relevant context; verify allocation
and the inputs needed before writes. Stay within its binding and allowed scope even
if CURRENT changes. Follow the [authority and local blocker rules](../SKILL.md#scope-and-authority);
propose record changes outside your write scope instead of applying them.

Return artifacts, self-checks, and a report ready for review: task/attempt and
delivery revision, binding, changed paths, retrievable versions, actual verification
results, limitations, and next recommendation. Include applicable resource usage
and unfinished job handles/output locations; a time limit does not prove jobs stopped.
For continued repairs, use [repair and delivery](repair-loop.md); no redispatch is
needed merely because the same worker already returned an earlier version.

## Manager: collect and recover

Before retry or collection, reconcile existing allocation, receipts, deliveries,
and running jobs. Verify identity, allowed diff, actual evidence, and receiving
baseline against the inspected inputs. Relevant drift requires fresh applicable
verification. Retain the inspected delivery through existing version control or
a delivery copy; preserve evidence before temporary paths disappear. Copy approved
artifacts, not the worker's entire planning directory.

A task/attempt can have multiple explicit delivery revisions. An identical replay
of the same revision is a no-op; changed contents under that revision need
investigation. Continue repairs under the current assignment where safe. Reassign
with a new attempt only after the old writer is stopped or prevented from changing
accepted outputs, preserving its reports and checks. Plan changes require explicit
rebinding or a reasoned reuse check, not edits to the dispatched snapshot.

Reviewer completes the scoped check; only an authorized Manager accepts, and only
the designated writer changes progress. A success message, closed Issue, or merged
PR is not by itself a passing acceptance check.

## Verify the combined delivery

When deliveries must work together, verify the final combined state as well as
the task criteria. Bundled plans set `integration_required: true` and use
`check.task: integration`; `integration` is not a plan task ID/type. Existing CI,
an integration environment, or a suitable workspace can supply this check. A
separate Integrator agent, packet, or workspace is optional; use the
[integration template](../assets/integration-handoff.md) only for a needed handoff.

Identify selected deliveries, final source/input versions, actual checks/results,
review provenance, and unresolved risks. Retain failures. Conflict resolution or
other relevant changes require renewed affected task checks. Before acceptance,
confirm the receiving final state matches the checked state and that task/integration
evidence still applies. One pipeline can supply both scopes of evidence; passing
task checks alone does not establish integration. The validator cannot detect
content drift or omitted inputs.

For research, also check methodological compatibility and interpretation under
the [shared budget and fixed-method rules](research.md), not just successful commands.
