# Validation record

**English (US)** | [Português (Brasil)](VALIDATION.pt-BR.md)

Validation was performed on July 18, 2026, using the environment documented in
[`README.md`](README.md).

## Completed checks

- All four SHA-256 checksums in `data/SHA256SUMS` were verified.
- All six unit tests passed.
- The short QGA check completed ten generations with seed 42.
- The refactored QGA was compared with the original copy on a regression
  problem using the same seed, population, generation count, encoding, and
  objective function. Parameters, best fitness, and history matched exactly.
- After the licensing and provenance update, the executable AST of `qga.py`
  remained identical to the validated baseline; only comments and its module
  docstring changed.
- `notebooks/comparacao_eficiencia_qga_bits.ipynb` completed a full `nbconvert`
  execution and regenerated the figures.
- `notebooks/analise_estabilidade_lmi.ipynb` completed a full `nbconvert`
  execution with CVXPY 1.9.1, Clarabel 0.11.1, and SCS 3.2.11.
- A repository scan found no personal paths, credentials, leaked secrets, or
  internal editorial references in the published files.
- The QGA provenance was checked against upstream revision
  `d20ad57f0a2576a6c48d8c8c4f7870a6192275e8`. The complete upstream MIT
  License and historical source notice are included in `LICENSES/`.
- A wheel was built with isolated build dependencies, installed in a temporary
  target, and used for the deterministic smoke test. Its metadata reports
  `License-Expression: MIT`, and all five required license and third-party
  notice files are present under the wheel's `dist-info/licenses/` directory.

## Validation boundary

The complete GA/QGA optimizations were not repeated. The source set did not
contain the driver that executed them and wrote the `pickle` files. Validation
covers the archived results, post-processing, final simulations, figures,
LMIs, and the isolated behavior of the QGA implementation.
