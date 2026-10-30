# Bounded research task

Use the `bounded-agent-research` skill with the existing team coordinator.
Supply the concrete question, baseline, candidate write scope, immutable evaluator
and data hashes, metric, trial/time/compute budgets, and approved tools. If these
are missing, prepare the contract before executing trials. Assign independent
workers isolated candidate workspaces, retain every result, and stop at the first
budget, cancellation or integrity boundary. Return a reviewed candidate and
evidence; do not promote or deploy automatically.
