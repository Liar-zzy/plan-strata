# Research tasks

Keep the question, method, comparison basis, acceptance, and resource/stop boundary
explicit in existing research records or the plan. Identify the mode:

- **Exploratory:** bound the search/analysis and record what changed after seeing
  data. Adapt within that scope; do not present adapted findings as confirmation.
- **Confirmatory:** fix the primary comparison, metrics/analysis, uncertainty
  treatment, exclusions, and stopping rule before execution. Record prior data
  exposure and deviations; distinguish added exploration. A local plan is not
  formal preregistration. Changing a committed method needs a plan revision.

Use meaningful budget units such as experiments, comparisons, or compute time.
Share the total across workers and state whether fixed-analysis verification
reruns are permitted. No universal run count is required. Extra experiments or
searching for a positive finding cannot silently consume more scope or budget.

Retain evidence suited to the work: data/configuration/environment for computation,
verifiable sources and inclusion criteria for synthesis, assumptions and checked
arguments for proofs. Record seeds/repetitions where relevant and retain negative
results and reasons for abandoning approaches.

Separate activity completion and method validity from the scientific finding and
next decision (`continue`, `diagnose`, `revise`, `stop`). A valid activity can pass
acceptance with `not_supported` or `inconclusive` findings. Failure to observe improvement
alone proves neither equivalence nor absence of effect; invalid inputs require
diagnosis before scientific interpretation. Label synthetic fixtures and metrics;
do not claim a real experiment ran when only a demonstration did.
