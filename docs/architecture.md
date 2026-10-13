# Architecture in plain language

The repository has one job: turn a structured assessment into a transparent diagnostic without hiding judgment behind a complicated system.

## How information moves

1. **The input file describes what was observed.** Each dimension includes a maturity score, evidence quality, observations, evidence references, risks, and candidate actions.
2. **The framework gives those observations a common language.** It defines the seven dimensions, their weights, and the meaning of each score.
3. **Validation stops unsafe scoring.** Missing dimensions, unexpected dimensions, or out-of-range scores cause a clear error rather than a plausible-looking result.
4. **The engine calculates, but does not pretend to discover truth.** It creates maturity and evidence scores, ranks gaps with a published formula, and applies a few explicit relationship rules.
5. **The output carries its limits with it.** Every result repeats the major caveats so the number cannot easily become detached from its meaning.

## Why it is intentionally small

- JSON keeps inputs and outputs readable in any text editor.
- Python's standard library avoids installation and dependency complexity.
- A command line makes the scoring behavior executable without requiring a product interface.
- Explicit rules are easier to challenge and revise than hidden automation.
- There is no persistence layer because versioned files are enough for this learning-stage tool.

## What belongs outside the engine

Interviews, analytics audits, CRM inspection, journey mapping, business impact estimation, and recommendation design are human analytical work. The program can structure their outputs. It cannot replace them.

## Safe next architectural step

The next useful layer is not automatically a dashboard. It is a calibration workflow: have two assessors score the same evidence, compare disagreements, refine anchors, and record why scores changed. That tests the diagnostic's reliability before increasing its technical surface area.

