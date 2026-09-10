# Worker handoff — {{task_key}} / {{attempt}}

Use this as the Issue body, delegation message, or local packet. Follow the
specified Plan Strata skill and its parallel-handoff guidance. Retain a snapshot
at dispatch; Manager maintains live progress. Return the report to Manager.

## Identity and baseline

- Repository/source access and workspace or creation instructions: {{project}}
- Task key (project / plan ID / task ID): {{task_key}}
- Attempt and worker, or coordinator and allocation procedure: {{attempt}} / {{worker}}
- Plan path and SHA-256: {{plan}} / {{plan_sha256}}
- Source/input baseline, retrieval, and verification: {{baseline}}
- Skill location/version: {{skill}}
- Manager and authoritative progress location: {{manager}}

## Read first

{{context}}

## Bounded task

{{objective}}

- Input/dependency readiness, accepted versions, and any release conditions: {{dependencies}}
- Allowed writes, including the attempt's evidence/report location: {{write_scope}}
- Shared interface and resource constraints: {{constraints}}
- Verification and acceptance method: {{acceptance}}
- Budget for implementation/self-checks and any finite review/repair allowance;
  stop/block conditions and authorized external effects: {{budget}}

## Return contract

Write {{report}} with this identity and plan binding; changed paths; exact output
commit or file fingerprints and retrievable locations; commands, actual results
and exit codes; this attempt's budget usage in the agreed units (mark unknowns);
deviations, blockers/running jobs, limitations, and next action.
Return artifacts for review. Manager maintains task state and acceptance.
