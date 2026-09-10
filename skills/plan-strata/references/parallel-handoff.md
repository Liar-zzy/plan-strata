# Optional parallel handoffs

Keep this mode off until the user explicitly chooses delegation for the current
iteration/batch, including a received assignment within that approved batch. A
natural-language request such as "enable parallel handoffs for this iteration"
is sufficient; no skill configuration switch is required. A proposal request is
only a proposal. Reuse an existing batch authorization within its bounds; treat a
new iteration/batch as opt-in again unless the user explicitly authorized more.

Skill discovery, Git availability, and apparently independent tasks are not opt-in.
Offer the option when independent deliveries justify its coordination cost. Once
chosen, use the host's available delegation and shell/Git tools within existing
permissions. If those capabilities are unavailable, explain the gap and offer
manual packets or sequential execution. Opt-in does not grant paid-job, Issue,
push, publication, or default-branch merge authority.

## Manager: prepare and assign

1. Choose a small batch within one ready ex-plan. A task is ready to execute when its required
   inputs and accepted dependencies are available. Shared interfaces and data
   formats must be settled; distinct filenames alone do not establish independence.
   Declare write scopes and shared resources, including output directories, GPU,
   databases, and experiment budgets. Serialize overlap or revise the plan first.
2. Agree the batch, worker/resource limit, stop conditions, and integration method
   with the user unless already authorized. Choose the delivery channel separately:
   local files, a host's delegation message, or a reviewed external task/Issue.
   Git availability is only a workspace capability, not a mode trigger. Use isolated
   copies or worktrees for concurrent writers; branches in one directory do not
   isolate files, and worktrees do not isolate shared services or compute resources.
3. Fill the [worker packet](../assets/task-handoff.md) for each task. Pin the task's
   versioned plan path and code/input baseline (an existing commit plus any retained
   dirty inputs, or an identified delivery copy). No per-file digests are required.
   Include only relevant context; material must be readable in the
   recipient's environment. External posting additionally needs an identified
   target, permissions, and a privacy review. Apply the [cold-start gate](#cold-start-gate)
   to the actual handoff delivered through the chosen channel.
4. By default, before execution, confirm the owner, attempt, binding, and workspace
   allocation in authoritative progress. Publishing an unclaimed task does not start it. In its
   handoff prose record task/attempt → packet, workspace/output location, and any
   runtime/job or external task handle. This is a dispatch receipt, not another
   status table. Give each attempt a distinct report location; packets are immutable
   assignments, not live copies of progress. Retain the dispatched Issue/message
   snapshot so later edits cannot silently change a running attempt. Start only
   within the agreed capacity.

Readiness and write-scope checks here are Manager judgments. Protocol v2's validator
checks declared records and acceptance; it does not lock claims, enforce readiness
at launch, or parse packet Markdown. Cross-ex-plan dependencies are outside this
first mode. Historical revisions are not additional tasks to dispatch.

## Ownership and progress bookkeeping

An explicit user assignment can supply the owner; Manager records that allocation
without asking the user to repeat it or issuing a second task brief. Opening an
Issue or creating a worktree alone supplies neither exclusivity nor permission.

Delayed progress recording is a project-specific opt-in, not the default workflow.
Use it only with an agreed allocating coordinator that reserves the task/attempt,
workspace, and shared resources before execution. Retain a recoverable assignment
receipt and packet/start snapshot in the chosen channel; every dispatcher must
reconcile that reservation before launch or retry. Manager remains the sole
progress writer and reconciles the receipt before acceptance or further dispatch.
A stale `planned` row is not proof that a task is free. Without those guarantees,
use the default pre-execution registration or return the ownership ambiguity.

## Cold-start gate

A complete handoff lets a recipient with no prior conversation use the task/Issue
and its accessible references to identify the work, verify entry conditions,
create or locate an isolated workspace, execute the bounded task, test it, and
return evidence. Core task instructions are ready before pickup; assignment
bookkeeping may happen at pickup.

For Issue dispatch, the Issue is the worker packet: put the objective, boundaries,
entry conditions, acceptance, and return contract in its body. Detailed plans and
supporting context may be linked at exact, retrievable versions. For Git-based
pickup, identify the repository, a fetchable ref containing the pinned commit,
and paths at that commit; a moving branch name alone is not a baseline.
Verify required documents are available there. Manager-only paths or uncommitted
files need an identified accessible delivery, not just a Manager-local filename.
If required material cannot be delivered within existing authority, explain the
block; publishing or pushing it needs the corresponding permission.

Describe packet completeness, dependency readiness, and assignment separately in
handoff prose; these are not new protocol states or a second progress table.
A complete, ready task can be unclaimed: specify the allocating coordinator and
how ownership is confirmed, following [the coordination rule](#ownership-and-progress-bookkeeping),
and how the worker creates its workspace, instead of requiring an existing worker
directory. Execution waits for that confirmation, not for another task brief.
An authorized draft or dependency-blocked Issue can be created early, with the
missing inputs and release conditions stated. When dependencies are accepted,
Manager pins their actual deliveries and confirms readiness before dispatch;
an upstream Issue closing alone does not release downstream work. Preserve earlier
snapshots when completing or revising the packet.

Before presenting a handoff as executable, inspect it from the recipient's entry
point: all essential content is inline or retrievable, baseline and start conditions
are verifiable, and scope, acceptance, budget, and report destination are concrete.
If this gate fails, return an explicitly incomplete/blocked handoff with the missing
items. Passing it neither launches an agent nor claims the task automatically.

## Worker: execute the bound assignment

Read the packet, applicable project instructions, and the pinned plan/core. Verify
the relevant baseline and assignment confirmation before task writes. Create a
workspace from the pinned inputs using the packet's instructions if none is supplied.
If the packet and assignment disagree, an
input is inaccessible, or a required dependency is not accepted, report the block
to Manager. CURRENT changing does not silently rebind this attempt.

Work in the assigned workspace and write scope. Manager retains authority over
core, plans, CURRENT, and progress; return proposed changes to those records instead
of editing them from a worker copy. Checks or reports belong in the allocated
attempt location. Stop and return a blocker if the task needs another worker's
scope, a changed interface, extra resources, or a new external action.

Include self-checks and any permitted repairs using [bounded repair](repair-loop.md).
Manager can continue that loop within the batch's existing scope and budget.

Return the identity/binding, changed paths, retrievable delivery versions/locations,
actual verification commands/results, report location, limitations, and
next recommendation specified by the packet. Distinguish a delivery ready for
review from an accepted task. Keep any running job handle and output location in
the report; reaching a time limit is not evidence that the job stopped.

## Manager: collect and recover

Before copying or accepting, compare the receiving workspace's relevant inputs
against the pinned baseline as well as checking the worker's identity, allowed
diff, and evidence. Check additions, removals, and changes to code, tests, shared
contracts, data, and configuration. Drift requires review and a fresh applicable
check, not acceptance under changed inputs. Separate live progress notes from
frozen inputs, while retaining task bindings and Manager's authority.

Keep the inspected delivery retrievable, using existing version control or a
retained delivery copy as appropriate. Copy approved artifacts, not
a worker's entire planning directory; evidence at temporary paths must be retained
or represented by a durable manifest before relying on it.

Reconcile an interrupted attempt from progress, the dispatch receipt, workspace,
and runtime/task handle before starting another. The same received result is a
no-op after its identity and unchanged delivery are confirmed; a changed result under the same
attempt requires investigation. Reassign only after the old attempt is stopped or
otherwise prevented from writing accepted outputs. Preserve its packet, reports,
and checks; allocate a new attempt. Revisions require explicit reassignment or a
reasoned reuse check, not edits to a running packet.

Manager alone updates progress through review and acceptance. A worker's success
message, an Issue closing, or a PR merging is not a passing task check.

## Integrator: verify the combined delivery

Set `integration_required: true` in the ready plan when deliveries must work
together. After required worker deliveries have applicable passing task checks,
Manager fills the [integration packet](../assets/integration-handoff.md) with their
exact artifacts and a separate integration workspace. Integrator is a terminal
role/gate, not a new protocol task type or a requirement that the round be complete
before it can start. Reserve `integration` for the check's task field; use ordinary
IDs such as T01 for plan tasks. Existing types remain development and research.

Integrator combines only the selected artifacts using the agreed method and runs
the acceptance checks on that final combined state. Its report identifies the
included deliveries, final source/input versions and locations, actual commands,
results, unresolved risks, and a proposed integration check with `task: integration`.
Include relevant inputs as explicit check subjects. Path lists neither discover
omissions nor prove unchanged contents; assess both during review. Use existing
Git diffs or direct inspection/comparison where needed, without digest bookkeeping.
Keep mutable progress out of that input set. The helper cannot perform this review.
If conflict resolution changes inspected code, refresh affected task checks before
accepting the final result. A review that also fixes code records that provenance.

On failure, retain the failing report/check and return the affected scope to Manager
for bounded repair or replanning. Writing a report is not passing integration.
Before recording `integration_check`, Manager rechecks the receiving final tree
against the exact state the Integrator inspected, confirms task evidence and input
coverage still apply, and makes the final handoff. Integrator may recommend
acceptance but does not publish, change Manager's progress, or merge a default
branch without that specific authority.

For research, use [research guidance](research.md): allocate a shared total budget
across workers, fix data/configuration/comparison inputs, and state whether exact
verification reruns are permitted. Integration checks methodological compatibility
and interpretation, not just successful commands. Preserve valid negative findings;
extra runs seeking a positive result need new scope and budget.
