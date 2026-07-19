# Avisos de terceiros

[English (US)](THIRD_PARTY_NOTICES.md) | **Português (Brasil)**

## QGA de R. Lahoz-Beltra

`src/qga_maglev/qga.py` contém trechos modificados derivados de `QGA.py` do
[ResearchCodesHub/QuantumGeneticAlgorithms](https://github.com/ResearchCodesHub/QuantumGeneticAlgorithms),
na revisão `d20ad57f0a2576a6c48d8c8c4f7870a6192275e8`. A implementação é
atribuída a R. Lahoz-Beltra e foi publicada sob a licença MIT, Copyright (c)
2016 ResearchCodesHub.

O cabeçalho histórico de `QGA.py` afirma que o software pode ser usado para
educação e pesquisa. A mesma revisão upstream inclui uma licença MIT para o
repositório. Esta distribuição preserva ambos os textos sem alterá-los:

- `LICENSES/QGA_UPSTREAM_NOTICE.txt` preserva o cabeçalho e a proveniência;
- `LICENSES/ResearchCodesHub-QuantumGeneticAlgorithms-MIT.txt` preserva a
  licença upstream integral.

A adaptação acrescenta função de aptidão externa, limites dos parâmetros e
dimensionamento configurável do cromossomo, semente determinística, validações
e tipagem, histórico da otimização e memória explícita do melhor global. Ela
também remove a interface interativa e os gráficos da implementação original.
Essas modificações são licenciadas sob a licença MIT da raiz, Copyright (c)
2026 Israel da Silva Felix de Lima, sem remover o copyright e os avisos
upstream.

## geneticalgorithm

Os experimentos históricos usaram `geneticalgorithm==1.0.2`, Copyright 2020
Ryan (Mohammad) Solgi, distribuído sob licença MIT. A cópia encontrada nos
arquivos de trabalho era byte a byte igual ao pacote instalado e, por isso, não
foi vendorizada neste repositório.

Projeto original: <https://github.com/rmsolgi/geneticalgorithm>
