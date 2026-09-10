# Bounded repair

Keep implementation, self-checks, and in-scope repairs within one observable task
outcome. A repair loop uses existing authority; it neither enables delegation nor
changes an explicit instruction to stop after a particular stage.

## Set the boundary

Include the outcome's entry paths, allowed writes, acceptance method, and finite
repair/resource budget in the task or packet. Use units suited to the work, such
as elapsed time, test runs, or review/repair rounds. State what consumes the budget
and count across retries and workers; a new attempt does not reset it. Reuse agreed
limits; otherwise state a proportionate limit for already-authorized local work.
Broader scope or external effects still need their own authority.

At handoff, retain used/remaining totals and any pending resource reservations in
existing progress; workers return their own usage in the agreed units and any
unfinished jobs. On recovery, reconcile reports/logs and job handles before spending
more. Unknown consumption is not zero: establish that the next action fits the
remaining allowance, or report the unresolved budget. No second budget tracker is
needed; Manager owns the shared total, or the single agent maintains it in progress.

## Implement, inspect, repair

1. Implement and self-check before formal delivery. Keep ordinary local patches
   and test iterations in the active task; record useful observations at milestones
   and retain relevant failing logs. Each edit needs neither a separate report,
   a frozen check, a plan revision, nor a progress-only commit.
2. For review findings, identify every blocker against the original acceptance
   criteria and affected inputs/entry paths. Separate non-blocking suggestions and
   new requests from defects in the agreed outcome. Explain the missing behavior
   and a reproducer or counterexample; related findings can share one repair.
3. Verify the affected paths and appropriate regressions. Reuse earlier passing
   findings only while their inputs and assumptions remain applicable; inspect
   affected earlier findings again. Review breadth follows risk and the selected
   review method, not a mandatory fresh reviewer team. Other applicable skills'
   requirements still apply.
4. Continue authorized repairs until acceptance or the agreed boundary. If the
   same defect recurs, examine the full relevant path and why the previous check
   missed it before spending another round. On exhausted budget, changed scope,
   uncertain ownership, or a decision needing new authority, preserve the result
   and report the specific next decision instead of silently extending the loop.

In an opted-in batch, Manager can inspect a worker return, arrange a bounded repair,
and accept the result within existing authorization. A worker stopping or delivering
is a Manager checkpoint, not automatically a pause for new user instructions. Use
available communication tools. A manual transport still needs a person to relay
messages; disclose that limitation.

## Preserve delivery identity and evidence

Before formal return, a worker may iterate within its current assignment and
budget. After return, retain the exact delivered inputs/outputs and report. For a
changed execution result, Manager uses a new attempt and report location under
the same task/plan when the scope still applies; confirm the previous writer has
stopped or is excluded before dispatch. Follow [collection and recovery](parallel-handoff.md#manager-collect-and-recover)
for delegated attempts. A new attempt is bookkeeping, not automatically new user
authorization. Never silently replace a received result under its old identity.

Create a new scoped check when accepting a delivery or changing an acceptance
decision, preserving old checks and their evidence. Relevant inspected inputs
changing also requires fresh applicable verification and a new check, even for
`pass` → `pass`. Updating hashes alone is not verification. Single-agent work can
keep internal progress and observations together without worker packets; freezing
a check does not make every later local edit a new delegated attempt.

## Example: one capability, bounded repairs

A task requires configuration validation at both startup and per-turn entry.
Its packet allows implementation/self-checks plus at most two Manager-requested
repair rounds for defects in that same behavior, within the shared time/test
budget. A round is one grouped repair request and the review of its return.

The first return covers per-turn validation but misses startup. Manager retains
that delivery and a failing check, then allocates a repair attempt covering the
startup path and associated regressions. After actual tests and review, a new
passing check can accept the same task without a plan revision or an extra human
approval. A logging-style suggestion remains non-blocking; a request for a new
configuration source is separate scope. Exhausting the limit with a remaining
blocker leaves the task open with the evidence and next decision recorded.

For research, use [research guidance](research.md): repair invalid execution or
analysis within its authorized method and recomputation budget. A valid negative
or inconclusive finding is not a defect to repair. Changing metrics or adding
experiments to seek a positive finding requires a separate justified decision.
