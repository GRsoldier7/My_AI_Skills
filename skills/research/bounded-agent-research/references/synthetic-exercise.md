# Synthetic tabletop exercise

This fixture exercises decisions; it does not execute an evaluator or model job.
Use the example contract and ledger. Baseline score is 4; candidate A scores 2
under the same evaluation and zero spend. Candidate B times out and has no score.
Candidate C changes the evaluator: invalidate it without using any reported score.
Expected result: A is the best verified candidate; B remains a recorded failure;
C is invalid; no further trial is started after the third attempted trial or any
earlier stop boundary. Promotion remains a review decision.

Additional expected outcomes: denied runtime yields a proposed experiment only;
changed metric/data hashes stop the run; unexpected paid API need stops before
spend; an unconfirmed cancellation stays pending and cannot trigger a duplicate
fallback; a restarted coordinator reconciles state before launching anything.
