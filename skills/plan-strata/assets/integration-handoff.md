# Integration handoff — {{plan_id}} / {{attempt}}

This terminal assignment proposes an integration verdict to Manager. Follow the
installed Plan Strata skill and its parallel-handoff guidance.

## Bound inputs

- Project and integration workspace: {{project}}
- Plan path and SHA-256: {{plan}} / {{plan_sha256}}
- Skill location/version: {{skill}}
- Manager and authoritative progress location: {{manager}}
- Required deliveries, accepted task checks, exact versions/hashes: {{deliveries}}
- Final input/source manifest or commit to verify: {{baseline}}
- Relevant instructions, core, plan sections, and prior reports: {{context}}

## Integration assignment

- Combination method and allowed writes: {{write_scope}}
- Whole-delivery acceptance checks: {{acceptance}}
- Resource budget, reruns, repair/stop boundary, and external permissions: {{budget}}

## Return contract

Write {{report}} identifying the incorporated deliveries, final source/input
fingerprints or commit, methods, actual results/exit codes, unresolved risks, and
next recommendation. Preserve evidence and propose a scoped check with
`task: integration`; a failed result remains a failed result. List the relevant
fixed input files as check subjects, not only a manifest's hash. If any inspected
input changes, identify the task checks needing renewal. Manager compares the
receiving final state with the inspected inputs before accepting, then updates
progress and decides delivery or repair.
