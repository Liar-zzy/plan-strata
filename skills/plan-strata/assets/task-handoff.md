# Worker handoff — {{task_key}} / {{attempt}}

This is an assignment snapshot, not a second progress record. Follow the installed
Plan Strata skill and its parallel-handoff guidance. Return the report to Manager.

## Identity and baseline

- Project and accessible workspace: {{project}}
- Task key (project / plan ID / task ID): {{task_key}}
- Attempt and assigned worker: {{attempt}} / {{worker}}
- Plan path and SHA-256: {{plan}} / {{plan_sha256}}
- Source/input baseline and how to verify it: {{baseline}}
- Skill location/version: {{skill}}
- Manager and authoritative progress location: {{manager}}

## Read first

{{context}}

## Bounded task

{{objective}}

- Required accepted inputs/dependencies: {{dependencies}}
- Allowed writes, including the attempt's evidence/report location: {{write_scope}}
- Shared interface and resource constraints: {{constraints}}
- Verification and acceptance method: {{acceptance}}
- Budget, stop/block conditions, and authorized external effects: {{budget}}

## Return contract

Write {{report}} with this identity and plan binding; changed paths; exact output
commit or file fingerprints and retrievable locations; commands, actual results
and exit codes; deviations, blockers/running jobs, limitations, and next action.
Return artifacts for review. Manager maintains task state and acceptance.
