---
name: plan-strata
description: Maintain versioned plans, execution handoffs, and evidence for software development and research work across sessions. Use when starting a bounded project iteration, resuming existing plans, revising an execution baseline, or checking completion. Simple questions and isolated small edits usually need no planning files.
license: MIT
metadata:
  version: "0.1.0-alpha.2"
---

# Plan Strata

Keep project intent, execution, and evidence connected across sessions. A single
execution plan can contain development and research tasks shared by several agents.
Use the user's language for project documents.

## Start or resume

1. Inspect project instructions and existing planning files. Preserve the project's
   established locations and terminology. Read [the protocol](references/protocol.md)
   when creating records, selecting a revision, or using the validator.
2. For an existing task, recover its recorded plan binding and handoff. For new
   work, follow `plans/CURRENT.md`. If the pointer is missing or inconsistent,
   report the ambiguity and resolve it from explicit project/user context;
   version ordering and modification time do not select a plan.
3. Read the selected core, execution plan, progress, and the evidence needed for
   the next action. Inspect actual files and running jobs where relevant to
   reconcile an interrupted handoff. State the next bounded action.
4. For a new iteration, adapt the [core](assets/core.md), [plan](assets/ex-plan.md),
   [progress](assets/progress.md), and [pointer](assets/CURRENT.md) templates.
   Fill actual goals and acceptance criteria before selecting a ready plan.
   Use existing authorization for work already in scope. Escalate a change in
   overall goals, resources, or external effects when it needs new authority.

## Execute and hand off

Parallel delegation is **off by default**. A user's explicit choice for the current
iteration/batch enables it; loading this skill or finding Git does not. For an
opt-in request, preparing or picking up an Issue/task handoff in an approved batch,
or terminal integration, read [parallel handoffs](references/parallel-handoff.md)
before publishing, assigning, or starting work. Ordinary work uses the workflow
below without extra packets.

- Put task definitions and dependencies in the plan; maintain live state only in
  progress. Record a plan path and content hash when starting a task. That binding
  survives later changes to CURRENT.
- Keep one progress writer per iteration. Workers share the plan, own distinct
  tasks, and submit separate reports when concurrent execution needs them.
  Concurrent code writers also need an explicit integration method and isolated
  outputs; the skill does not supply a scheduler or a lock.
- Use a complete observable outcome as the task unit. For task budgeting,
  review-driven repairs, or resuming a repair loop, read [bounded repair](references/repair-loop.md).
  Internal patches and milestones are not automatic human approval gates.
- At a meaningful milestone, blocker, or handoff, record what changed, where the
  artifacts are, what was checked, what remains uncertain, and the next action.
  Record a running job's identifier and output location before yielding it.
  Single-agent work can keep this in progress; create `reports/` when needed.
- For development tasks, read [development guidance](references/development.md)
  before defining acceptance or accepting a delivery. For research tasks, read
  [research guidance](references/research.md) before planning or interpreting
  evidence. Mixed plans use both; each task retains its own acceptance meaning.

## Check and decide

1. At an acceptance decision, inspect the actual result using the plan's acceptance
   method. An execution report is a starting point for verification. Record a
   scoped conclusion in a new [check](assets/check.md), including the bound plan,
   inspected subjects, evidence, method, limitations, and next decision. Preserve earlier checks.
2. Mark a task `done` only when its applicable check passes and dependencies allow
   acceptance. A valid research activity can be done with an inconclusive or
   negative finding. Check integrated behavior separately when the plan requires
   it. Record review provenance; another agent is optional, not proof by itself.
3. For the bundled metadata format, run:

   ```text
   python3 <skill-directory>/scripts/strata.py validate --project <project-directory>
   ```

   Fix inconsistent records. This read-only command verifies references, selected
   file hashes, and state consistency. `consistent` does not mean tests ran,
   evidence is truthful, or the research claim is established. Inspect `overall`
   separately. Existing alternative formats may be checked manually without
   migration; disclose that the bundled validator was not used on them.
4. Report the outcome, remaining limitations, and justified next action. Stop or
   replan when the agreed budget or decision boundary is reached.

## Revise

Keep a round's identity (for example `P001`) separate from its revision. Add a new
plan revision for changed scope, dependencies, methods, or acceptance criteria;
update progress for ordinary execution. Change core when project intent or key
constraints change. Read the protocol's revision rules before changing a selected
baseline. Write the reason and affected tasks into the new plan.

Keep started revisions available with their exact bytes. Select the new ready
revision explicitly, then reconcile pending work and previous acceptance. Running
tasks retain their bindings until explicitly continued, stopped, or reassigned.
Use a new check to justify reuse under changed criteria. Preserve historical
results while marking current acceptance `needs_review` when applicability is
uncertain.
