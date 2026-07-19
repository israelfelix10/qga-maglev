# QGA tuning of fuzzy controllers for a MAGLEV system

**English (US)** | [Português (Brasil)](README.pt-BR.md)

Research code and artifacts for evaluating a quantum-inspired genetic
algorithm (QGA) in the tuning of type-1 (FT1) and interval type-2 (IT2-FLC)
fuzzy servocontrollers for a magnetic levitation system.

Using the archived results, this repository reproduces the final simulations,
performance metrics, convergence curves, figures, and LMI-based stability
analysis. It also provides the QGA implementation used in the study and a
short deterministic experiment for checking execution and reproducibility.

Code comments and docstrings are provided in both Brazilian Portuguese and
US English. The PT-BR text appears first, followed by its EN-US counterpart.

## Relationship to the published research

This repository is associated with the following conference chapter:

> I. da Silva Felix de Lima and F. Meneghetti Ugulino de Araújo,
> “[Quantum Genetic Algorithm Tuning of Interval Type-2 Fuzzy State Feedback
> Controllers for MAGLEV Servosystems](https://doi.org/10.1007/978-3-032-15632-7_29),”
> in *Computational Intelligence — IJCCI 2025*, CCIS 2827, pp. 531–548,
> Springer, 2026.

The chapter was first published online on January 28, 2026. Although the
repository follows the same research line, it is **not a frozen replication of
the materials available when the chapter was published**. It includes
methodological, computational, analytical, and documentation developments
added afterward. Any differences should therefore be understood as later
developments of the work, subject to the conditions and limitations documented
here.

When using results reported in the chapter, cite the publication. When using
the code, data, or post-publication analyses from this repository, also cite
the repository and identify the version used.

## Reproducibility scope

The source set did not include the driver that instantiated the GA and QGA and
wrote the four `pickle` files. Therefore, this version **does not claim to
regenerate the complete optimization runs from scratch**. The archived
optimization results are preserved in `data/`, protected by SHA-256 checksums,
and serve as inputs to the reproducible analyses.

The distinction is as follows:

- reproducible: archive inspection, simulations with archived poles, metrics,
  figures, convergence analysis, and LMIs;
- independently verifiable: chromosome decoding and deterministic QGA
  execution with a fixed seed;
- not reconstructed: the original orchestration driver that ran every
  optimization and generated the `pickle` files.

## Repository layout

```text
data/                  precomputed results and checksums
notebooks/             results analysis and LMI stability verification
results/figures/       selected final figures
scripts/               inspection, validation, and artifact generation
src/qga_maglev/        QGA implementation and utilities
tests/                 unit and reproducibility tests
LICENSES/              upstream QGA license and provenance notices
```

The byte-identical notebook backup, Python caches, the local copy of the
`geneticalgorithm` package, and four obsolete figures were excluded.

## Environment

The published copy was validated with:

- Windows 11;
- Python 3.12.5;
- NumPy 2.0.2;
- SciPy 1.16.3;
- Matplotlib 3.10.0;
- `geneticalgorithm` 1.0.2;
- `func-timeout` 4.3.5;
- CVXPY 1.9.1;
- Clarabel 0.11.1;
- SCS 3.2.11;
- nbformat 5.10.4 and nbconvert 7.17.1.

These versions describe the environment used to clean and validate the
repository. Not every dependency version was recorded in the historical
artifacts, so this list is not proof of the exact environment used for each
original run.

### Windows installation

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

### Linux or macOS installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

## Archived configuration

All result archives record global seed `42`, a population of `30`, and `50`
generations.

| Parameter | Classical GA | QGA |
|---|---:|---:|
| Seed | 42 | 42 |
| Population | 30 | 30 |
| Generations | 50 | 50 |
| Mutation | 0.15 | 0.01 per individual; 0.001 per gene |
| Crossover | 0.70 | not applicable |
| Elitism | 0.05 | global-best memory |
| Bits per parameter | not applicable | 10, 16, 24, or 32 |
| Measurement threshold | not applicable | 0.5 |

The four pole parameters use bounds `[5, 50]`, `[5, 50]`, `[5, 50]`, and
`[1, 30]`. The optimization objective uses a 5-second simulation; the final
simulations use 10 seconds and a 2 ms controller step. Metrics computed over
these two horizons must not be compared directly.

## Running the repository

Run the following commands from the repository root.

### 1. Check data integrity and run tests

Checksum verification does not deserialize the `pickle` files:

```powershell
python scripts/verify_data.py
python -m unittest discover -s tests -v
```

Run the short deterministic QGA check:

```powershell
python scripts/qga_smoke.py --seed 42
```

This check uses a synthetic objective function; it is not a new MAGLEV plant
optimization.

### 2. Inspect archived results

```powershell
python scripts/inspect_results.py
```

The command displays recorded seeds, configurations, ITAE values, and run
times. Read the `pickle` security warning below before running it.

### 3. Reproduce the analysis and figures

```powershell
New-Item -ItemType Directory -Force results\notebooks | Out-Null
python -m nbconvert --to notebook --execute `
  notebooks\comparacao_eficiencia_qga_bits.ipynb `
  --output comparacao_eficiencia_qga_bits.executado.ipynb `
  --output-dir results\notebooks `
  --ExecutePreprocessor.timeout=-1
```

The notebook reads the four files in `data/` and writes figures to
`results/figures/`. Version-controlled notebooks do not contain embedded
outputs.

### 4. Run the LMI stability analysis

```powershell
python -m nbconvert --to notebook --execute `
  notebooks\analise_estabilidade_lmi.ipynb `
  --output analise_estabilidade_lmi.executado.ipynb `
  --output-dir results\notebooks `
  --ExecutePreprocessor.timeout=-1
```

The notebook checks the local closed-loop systems and searches for a common
quadratic Lyapunov matrix over selected operating windows. Feasibility is
numerical and depends on the formulation, grid, and solver; it is not a global
proof outside the evaluated conditions.

### 5. Regenerate the summary metrics figure

```powershell
python scripts/regenerate_metrics.py `
  --output results\figures\comparacao_metricas_desempenho.png
```

The figure uses the documented 10-second final metrics, not the 5-second
optimization objective values.

### Linux or macOS command equivalents

```bash
python scripts/verify_data.py
python -m unittest discover -s tests -v
python scripts/qga_smoke.py --seed 42
python scripts/inspect_results.py

mkdir -p results/notebooks
python -m nbconvert --to notebook --execute \
  notebooks/comparacao_eficiencia_qga_bits.ipynb \
  --output comparacao_eficiencia_qga_bits.executado.ipynb \
  --output-dir results/notebooks \
  --ExecutePreprocessor.timeout=-1

python -m nbconvert --to notebook --execute \
  notebooks/analise_estabilidade_lmi.ipynb \
  --output analise_estabilidade_lmi.executado.ipynb \
  --output-dir results/notebooks \
  --ExecutePreprocessor.timeout=-1

python scripts/regenerate_metrics.py \
  --output results/figures/comparacao_metricas_desempenho.png
```

## Regression values

Reference values used to check the final analysis include:

| Configuration | Final ITAE |
|---|---:|
| Original FT1 | 1.6003e-3 |
| Original IT2-FLC | 1.5819e-3 |
| FT1 + GA | 6.3559e-4 |
| IT2-FLC + GA | 6.0970e-4 |
| FT1 + QGA, 32 bits | 6.1251e-4 |
| IT2-FLC + QGA, 32 bits | 6.0509e-4 |

Run times depend on the hardware and software environment. Convergence times
obtained by proportional allocation are estimates, not wall-clock
measurements from a run stopped at the reported generation.

## Data security

`pickle` files may execute code while being deserialized. Load only the files
provided by this repository and first verify their checksums with
`python scripts/verify_data.py`. Do not use `inspect_results.py` or the
notebooks to open untrusted third-party `pickle` files.

## Licensing and attribution

Source code in this repository is licensed under the MIT License.
`src/qga_maglev/qga.py` contains modified portions derived from
[ResearchCodesHub/QuantumGeneticAlgorithms](https://github.com/ResearchCodesHub/QuantumGeneticAlgorithms)
at revision `d20ad57f0a2576a6c48d8c8c4f7870a6192275e8`. The upstream
implementation is attributed to R. Lahoz-Beltra and is distributed under the
MIT License, Copyright (c) 2016 ResearchCodesHub. The historical source header
and complete upstream license are preserved in
`LICENSES/QGA_UPSTREAM_NOTICE.txt` and
`LICENSES/ResearchCodesHub-QuantumGeneticAlgorithms-MIT.txt`. See
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for attribution and
modification details.

The classical GA backend is the external package
`geneticalgorithm==1.0.2`, by Ryan (Mohammad) Solgi, under the MIT License. The
vendored duplicate was removed.

The archived data and generated figures are research artifacts, not software,
and are not covered by the software MIT License. They are provided for
verification under the rights statements in `data/README.md` and
`results/README.md`; no separate open-data or open-content license is granted.

## Citation

Citation metadata are provided in `CITATION.cff`. When reusing results, also
cite the associated conference chapter and report the bit resolution, seed,
repository version, and comparison protocol.

## Author

Israel da Silva Felix de Lima, 2026.
