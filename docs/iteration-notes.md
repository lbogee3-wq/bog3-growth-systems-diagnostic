# Iteration notes: first pass, failures, and improvement

## Build sequence

1. Defined the repository purpose and boundaries.
2. Defined a seven-dimension input model and maturity framework.
3. Built the smallest executable first pass in `src/diagnostic_v1.py`.
4. Ran it against both synthetic examples.
5. Examined what the output concealed or overstated.
6. Built the improved version in `src/diagnostic.py` and added focused tests.
7. Generated and committed improved outputs.

## What the first pass did

V1 read the dimension scores, calculated a simple average, and returned the three lowest dimensions.

That proved the smallest end-to-end path: file in, calculation, diagnostic-shaped output. It was useful as executable scaffolding and inadequate as a responsible diagnostic.

## What failed or was limited

1. **Weak evidence looked identical to strong evidence.** The arithmetic average implied more confidence than the input supported.
2. **Invalid inputs could produce plausible output.** Missing dimensions or out-of-range scores were not checked.
3. **It treated dimensions as isolated categories.** It could not surface conversion without follow-up, or higher-maturity claims resting on weak measurement.
4. **“Lowest” was not a sufficient priority model.** It ignored evidence uncertainty and gave no reason for the rank.
5. **The output was too easy to overread.** It did not carry enough limitations or make synthetic status prominent.
6. **The framework was implicit in code.** A reviewer could not easily inspect weights, questions, or score meanings.

## What improved

- Added strict validation for required dimensions, integer score ranges, evidence ranges, and list fields.
- Separated maturity from evidence coverage instead of blending them into false precision.
- Moved framework definitions and equal weights into a readable JSON file.
- Added a published priority formula and explains what it does not measure.
- Added three explicit cross-system rules whose reasoning can be inspected.
- Included observations, evidence, risks, candidate actions, synthetic status, and caveats in output.
- Added tests for expected calculations, deterministic priorities, validation failures, and a relationship rule.

## What still fails by design

The improved version still cannot determine whether an assessor chose the right score, whether evidence is true, what a gap costs, or which intervention will create value. It has no external benchmarks and no empirical calibration. Those limitations should be resolved through evidence practice and calibration before adding technical complexity.

