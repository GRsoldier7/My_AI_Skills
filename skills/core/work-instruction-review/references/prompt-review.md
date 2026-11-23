# Prompt revision for repeatable work

Identify what failed: missing evidence, wrong metric, wrong audience, unwanted extra text or an invented tool action. Preserve constraints that worked. Remove repeated instructions, specify the input boundary, state the decision to make, and give an observable answer format. Use one example when it resolves a genuine ambiguity.

**Example revision.** Replace “review my numbers and make it sound good” with the following prompt.

> Using only the supplied synthetic rows, show completed, eligible and the overall completion rate. Compute the total from counts. Flag a missing denominator and return the question needed to resolve it. Give the manager one sentence and a small table.

Compare baseline and revision on the same cases, in independent fresh chats when possible. Use 1/2 and 2/8 (overall 30%), a zero denominator (undefined), and an unrelated request (keep the procedure out of it). Record arithmetic correctness, false claims, significant edits and output length. Keep a held-out case with unequal denominators. Retain the shorter version when quality ties. API access is unnecessary for this comparison. The optional upstream Copilot prompt-format reference applies when preparing an actual Copilot prompt file.
