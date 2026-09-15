# Integration handoff — {{plan_id}} / {{attempt}}

Use only when a separate handoff is useful; existing CI or the responsible agent
can perform integration without another agent/workspace. Follow {{skill}}.

- Project and verification environment/workspace: {{project}}
- Plan binding: {{plan}}
- Manager, designated progress writer, and record location: {{manager}}
- Selected deliveries, applicable task checks, and retrievable versions: {{deliveries}}
- Final source/input state to verify: {{baseline}}
- Relevant context not already recovered: {{context}}
- Combination method and allowed writes: {{write_scope}}
- Whole-delivery acceptance checks: {{acceptance}}
- Applicable limits, rerun/stop conditions, and external permissions: {{budget}}

Return via {{report}}: included deliveries, inspected final state, actual methods,
results/exit codes, review provenance, limitations, and proposed verdict. Retain
failed evidence. For bundled records, propose a check with `task: integration`
and explicit relevant input paths; identify task checks invalidated by changes.
Manager confirms the receiving state matches the checked state and decides
acceptance; only the designated writer records progress.
