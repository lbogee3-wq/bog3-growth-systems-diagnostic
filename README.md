# BOG3 Growth Systems Diagnostic

An intentionally small, auditable diagnostic for examining whether a growth system works as a connected whole—not merely whether individual marketing activities exist.

It evaluates seven dimensions:

1. Acquisition / discovery
2. Conversion
3. Lifecycle / follow-up
4. Customer / patient experience
5. Measurement / data quality
6. CRM / MarTech
7. Organizational / process alignment

The tool produces two separate signals:

- **Maturity score (0–100):** how developed the assessed system appears to be.
- **Evidence coverage (0–100):** how much confidence the available evidence supports.

Keeping those signals separate is deliberate. Missing evidence is not proof of poor performance, and a confident score should not be manufactured from weak inputs.

## Intended use

Use this as a structured starting point for a growth-systems review: gather evidence, score each dimension against common anchors, surface constraints, and decide what to investigate or improve next. It is useful for advisory discovery, internal alignment, and learning.

It is **not** a benchmark, predictive model, automated strategy, compliance review, or substitute for stakeholder interviews and source-system validation. Scores are directional and depend on assessor judgment.

## Run it

Requirements: Python 3.10+; no third-party packages.

```bash
python3 -m src.diagnostic data/sample_bog3_synthetic.json
python3 -m src.diagnostic data/sample_birken_synthetic.json --output data/outputs/birken_diagnostic.json
python3 -m unittest discover -s tests -v
```

The first command prints JSON. The second saves it.

To see the deliberately naïve first pass:

```bash
python3 -m src.diagnostic_v1 data/sample_bog3_synthetic.json
```

## Input

Each assessment records:

- identifying context and an explicit `synthetic` flag;
- one `score` from 0–4 for every dimension;
- `evidence_quality` from 0–3;
- observations, evidence references, risks, and possible actions.

See [`data/input.schema.json`](data/input.schema.json), the synthetic examples in [`data/`](data/), and the scoring anchors in [`docs/framework.md`](docs/framework.md).

## Output

The final diagnostic returns:

- overall maturity and evidence coverage as distinct measures;
- dimension-level scores, evidence labels, and observations;
- ranked priorities using a visible formula;
- cross-system warnings based on explicit rules;
- limitations carried into every result.

Example results are committed under [`data/outputs/`](data/outputs/).

## Architecture

```text
data/input JSON
      |
      v
validate structure and score ranges
      |
      v
score dimensions + evidence separately
      |
      v
rank gaps + apply a few explicit system rules
      |
      v
JSON diagnostic
```

- `src/diagnostic_v1.py` — the smallest first pass, retained for comparison.
- `src/diagnostic.py` — validated and improved diagnostic engine and command line.
- `src/framework.json` — dimension definitions, weights, and maturity anchors.
- `data/` — input schema, clearly labeled synthetic examples, and generated outputs.
- `tests/` — focused behavior and validation tests.
- `docs/` — plain-language architecture, iteration record, and lessons.

The code uses only Python's standard library. There is no database, UI, API, account system, or hidden model.

## Important boundaries

- The sample organizations and all sample values are synthetic. Similarity to BOG3 or Birken Law is illustrative, not factual reporting.
- Equal default weights express a neutral starting assumption, not an empirical claim that every dimension always has identical business impact.
- The tool ranks investigation and improvement candidates; it does not prove causality.
- The repository does not contain client data.

## Learning trail

The build sequence, first-pass failures, improvements, and lessons are documented in [`docs/iteration-notes.md`](docs/iteration-notes.md) and [`docs/lessons-learned.md`](docs/lessons-learned.md). The plain-language component map is in [`docs/architecture.md`](docs/architecture.md).

