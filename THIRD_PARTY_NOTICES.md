# Third-party notices

**English (US)** | [Português (Brasil)](THIRD_PARTY_NOTICES.pt-BR.md)

## QGA by R. Lahoz-Beltra

`src/qga_maglev/qga.py` contains modified portions derived from `QGA.py` in
[ResearchCodesHub/QuantumGeneticAlgorithms](https://github.com/ResearchCodesHub/QuantumGeneticAlgorithms)
at revision `d20ad57f0a2576a6c48d8c8c4f7870a6192275e8`. The implementation is
attributed to R. Lahoz-Beltra and was published under the MIT License,
Copyright (c) 2016 ResearchCodesHub.

The historical `QGA.py` header states that the software can be used for
education and research. The same upstream revision includes an MIT License
covering the repository. This distribution preserves both texts without
altering either:

- `LICENSES/QGA_UPSTREAM_NOTICE.txt` preserves the source header and provenance;
- `LICENSES/ResearchCodesHub-QuantumGeneticAlgorithms-MIT.txt` preserves the
  complete upstream license.

The adaptation adds an external fitness function, parameter bounds and
configurable chromosome sizing, deterministic seeding, validation and typing,
optimization history, and explicit global-best memory. It also removes the
original interactive and plotting interface. These modifications are licensed
under the root MIT License, Copyright (c) 2026 Israel da Silva Felix de Lima,
without removing the upstream copyright and notices.

## geneticalgorithm

The historical experiments used `geneticalgorithm==1.0.2`, Copyright 2020 Ryan
(Mohammad) Solgi, distributed under the MIT License. The copy found in the
working files was byte-for-byte identical to the installed package and was
therefore not vendored in this repository.

Upstream project: <https://github.com/rmsolgi/geneticalgorithm>
