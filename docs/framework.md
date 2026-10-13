# Diagnostic framework

## First principle

A growth system is not a collection of channels. It is the relationship among how people discover an organization, take a next step, receive follow-up, experience delivery, generate usable data, move through supporting technology, and encounter organizational decisions and handoffs.

The diagnostic therefore looks for both capability within each dimension and constraints between dimensions.

## Maturity scale

| Score | Anchor | Meaning |
|---:|---|---|
| 0 | Absent | No reliable capability or evidence of a repeatable practice. |
| 1 | Reactive | Activity exists but is inconsistent, manual, or person-dependent. |
| 2 | Defined | A recognizable process exists, with material gaps or uneven adoption. |
| 3 | Managed | The process is consistently used, measured, and owned. |
| 4 | Adaptive | The system learns across functions and improves through reliable feedback loops. |

## Evidence scale

| Score | Label | Meaning |
|---:|---|---|
| 0 | None | Assertion only or evidence unavailable. |
| 1 | Limited | Anecdotal, partial, or not recently verified. |
| 2 | Supported | More than one relevant source or a directly observed source. |
| 3 | Strong | Triangulated, current, and directly tied to the scored capability. |

Maturity and evidence are intentionally not collapsed into one number. A seemingly mature capability with weak evidence should prompt verification, not an automatic downgrade presented as fact.

## Dimensions

| Dimension | System question |
|---|---|
| Acquisition / discovery | Can the right people reliably discover the organization through a coherent mix of channels? |
| Conversion | Can interested people take a clear next step with low friction, and can completion be distinguished from intent? |
| Lifecycle / follow-up | Are prospects and customers followed up with deliberately across stages, not only at the first transaction? |
| Customer / patient experience | Does the end-to-end experience feel coherent, understandable, and responsive to human needs? |
| Measurement / data quality | Can decisions rely on trustworthy definitions, collection, and interpretation of data? |
| CRM / MarTech | Do tools support the journey and the work without avoidable fragmentation or manual failure points? |
| Organizational / process alignment | Are ownership, decisions, handoffs, and operating rhythms aligned around the journey? |

## Calculations

- **Dimension maturity:** `score / 4 × 100`
- **Overall maturity:** weighted mean of dimension maturity; the starter framework uses equal weights.
- **Evidence coverage:** weighted mean of `evidence_quality / 3 × 100`.
- **Priority score:** `70% × maturity gap + 30% × evidence uncertainty`.

Priority is a triage signal. It does not estimate revenue impact, effort, causality, or strategic fit.

## Explicit cross-system rules

The improved version flags three interpretable patterns:

1. A high score in another dimension with measurement at 0–1: stronger claims may be difficult to verify.
2. Conversion at 2+ with lifecycle at 0–1: the system may create initial demand without reliable follow-up.
3. Organizational alignment at 0–1: channel or technology changes may not persist without clearer ownership and operating rhythm.

These are hypotheses to investigate, not conclusions.

