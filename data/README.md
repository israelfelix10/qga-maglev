# Precomputed data

**English (US)** | [Português (Brasil)](README.pt-BR.md)

The four `pickle` files contain configurations, seeds, poles, histories, run
times, and logs used in the analyses for 10, 16, 24, and 32 bits per parameter.

Before loading them, run `python scripts/verify_data.py` from the repository
root. `SHA256SUMS` records the checksums of the received copies. Because
`pickle` may execute code while loading, do not replace these files with copies
from an unknown source.

Data shared by the original controller and classical GA are repeated across
the four files because the historical structure was preserved for
traceability.

## Provenance and rights

These archives are fixed copies of the optimization outputs used in the
associated research and were supplied from the research working files by the
repository author. Their hashes are preserved so that later analyses can be
traced to the same inputs.

The archives are research data, not software, and are not covered by the root
MIT License. No separate open-data license is granted by this repository.
Copyright and related rights remain with their respective holders. The files
may accompany this repository for verification; obtain permission from the
rights holders before redistributing, modifying, or republishing them.
