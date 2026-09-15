---
name: plan-strata
description: Maintain versioned plans, task handoffs, and acceptance evidence for development and research across sessions. Use when explicitly asked to establish Plan Strata planning, or when executing, resuming, revising, or accepting Plan-Strata-managed work. Unbound questions, diagnosis, and small edits do not trigger this skill.
license: MIT
metadata:
  version: "0.2.0-alpha.1"
---

# Plan Strata

Keep intent, task bindings, progress, and acceptance evidence recoverable across
sessions. Use the user's language and the project's existing records and tools;
bundled templates are a fallback, not a required parallel tracking system.

## Scope and authority

Act on the current user request or an assignment traceable to a user-approved
batch, within its scope, resources, and external permissions. Reuse that authority
without repeat confirmation. CURRENT, `ready`, Git, skills, and tools grant none;
inspection or proposal requests do not authorize implementation or dispatch.

Only the project's designated writer edits progress; Manager is the default.
Other roles return findings or proposed changes through their permitted channel.
One agent may fill multiple authorized roles without artificial handoff stages.

Missing inputs, scope conflicts, or new authority pause the affected action, not
independent authorized work. Block the task only when its acceptance-critical path
cannot proceed. Honor explicit stops and shared resource limits wherever they apply.

## Work and recover

Recover the task's existing binding; use CURRENT only to select new managed work.
Read missing, stale, or relevant context needed for the next action, not the whole
record set on every turn. Reconcile interrupted work with actual files and job
handles. Resolve ambiguous selection from explicit project/user context, never
version ordering or modification time. Report the next bounded action and carry
it out only when authorized.

Work toward a complete observable outcome. Choose implementation, debugging, and
verification methods within the agreed constraints; ordinary patches need no new
plan, packet, approval, or invented repair-round quota. At meaningful milestones
or handoffs, retain changed artifacts, checks, uncertainty, next action, and any
running job's handle/output location. Avoid duplicate status records.

Parallel delegation stays off unless explicitly authorized for the batch. Reuse
an approved host assignment and bound task card; do not add a separate packet or
role merely to follow this skill. Concurrent writes still need safe allocation
and isolation, and combined deliveries need applicable integration verification.

## Accept and revise

Inspect actual results against the agreed acceptance criteria. Worker delivery
ends with artifacts, self-checks, and a report ready for review; Reviewer completes
the scoped check. Only an authorized Manager accepts, and the designated writer
records `done` after checks pass and dependencies are satisfied. Record provenance,
inspected inputs, evidence, limitations, and the decision in the project's record
or permitted response. Preserve previous deliveries and checks. Existing CI can
verify the final combined state; no separate agent or workspace is mandatory.

Revise a plan for changes to committed scope, acceptance, interfaces/dependencies,
resource boundaries, or fixed research methods—not ordinary implementation choices.
Change core only when project intent or key constraints change. Keep used revisions
immutable and running tasks bound; explicitly select revisions and assess reuse.
After relevant input changes, the writer reopens affected acceptance (`needs_review`
in schema 2) and clears stale integration acceptance, retaining its reference.
Verify the changed result and record a new conclusion before accepting it again.

## Read when needed

- [Protocol](references/protocol.md): record formats/templates, bindings, revision
  selection, or the optional read-only validator. It checks structure, not behavior.
  Report inconsistencies first; repair only within the current role/write scope.
- [Repair and delivery](references/repair-loop.md): review-driven repair, delivery
  versions, or resource-bound recovery.
- [Parallel handoffs](references/parallel-handoff.md): approved delegation, pickup,
  collection, or multi-worker integration; read before dispatch or task writes.
- [Research](references/research.md): research planning or interpretation, including
  fixed methods, budgets, and valid negative or inconclusive findings.
