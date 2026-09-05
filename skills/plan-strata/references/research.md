# Research tasks

Core states the research question, scope, key assumptions, and resource/stop
boundaries. The plan states this iteration's hypotheses or open questions,
methods, comparison basis, analysis, and budget. Exploration can generate new
hypotheses within a stable core. Change core when the project direction changes.

Before work, identify the mode:

- **Exploratory:** define the question and bounded search/analysis budget. Record
  what was tried and what changed after looking at data. Findings motivate later
  tests; avoid presenting an adapted analysis as a pre-specified confirmation.
- **Confirmatory:** specify the primary comparison, metric/analysis, relevant
  uncertainty treatment, exclusions, and stopping rule in advance. Record known
  prior exposure to the data. Preserve and explain deviations and distinguish any
  added exploratory analyses. A local plan file is not a formal preregistration.

Give the budget an explicit unit: new experiments, candidate methods, comparisons,
or compute time. State whether verification may recompute the same fixed analysis,
so accepting an artifact does not silently expand the research scope.

The output can be an experiment, literature synthesis, proof, or diagnostic
finding. Choose suitable evidence: data/configuration/manifests and environment
for computation; verifiable sources and inclusion criteria for literature;
assumptions and checked arguments for a proof. Record seeds and repeated runs
when the method needs them; a universal fixed run count is not required.

Keep these judgments separate:

1. **Execution:** was the agreed activity completed?
2. **Validity:** did the actual method, inputs, and analysis meet the stated checks?
3. **Finding:** what does the evidence support, and within what limits?
4. **Decision:** continue, diagnose, revise, or stop, with a reason and budget.

A check can pass while `research.finding` is `not_supported` or `inconclusive`.
That task may be done. Failure to find an improvement does not alone establish
equivalence, absence of an effect, or a general refutation. Invalid inputs or a
broken evaluation require diagnosis before scientific interpretation.

Retain negative results and the reasons for abandoning approaches. Let later
plans cite these findings. Do not spend beyond the agreed budget searching for a
positive result. Additional work needs a stated question and authorized scope.

Label synthetic fixtures and demonstration metrics explicitly. For test fixtures,
interpret their stated scenario without claiming a real scientific experiment ran.
