# QGA aplicado à sintonia de controladores fuzzy para MAGLEV

[English (US)](README.md) | **Português (Brasil)**

Código e artefatos de pesquisa usados na análise de eficiência de um algoritmo
genético de inspiração quântica (QGA) na sintonia de servocontroladores fuzzy
tipo-1 (FT1) e tipo-2 intervalar (IT2-FLC) para um sistema de levitação
magnética.

O repositório permite reproduzir, a partir dos resultados arquivados, as
simulações finais, métricas, curvas de convergência, figuras e a verificação de
estabilidade por LMIs. Ele também contém a implementação do QGA empregada no
estudo e um experimento curto para verificar sua execução e sua
reprodutibilidade.

Os comentários e as *docstrings* do código são apresentados em português do
Brasil e em inglês dos Estados Unidos, sempre com o texto em PT-BR primeiro e
seu correspondente em EN-US na sequência.

## Associação com a pesquisa publicada

Este repositório está associado ao capítulo de conferência:

> I. da Silva Felix de Lima e F. Meneghetti Ugulino de Araújo,
> “[Quantum Genetic Algorithm Tuning of Interval Type-2 Fuzzy State Feedback
> Controllers for MAGLEV Servosystems](https://doi.org/10.1007/978-3-032-15632-7_29),”
> em *Computational Intelligence — IJCCI 2025*, CCIS 2827, pp. 531–548,
> Springer, 2026.

O capítulo foi publicado on-line em 28 de janeiro de 2026. Embora compartilhe
a mesma linha de pesquisa, este repositório **não é uma réplica congelada do
material existente na data da publicação**: ele inclui desenvolvimentos
metodológicos, computacionais, analíticos e de documentação incorporados
posteriormente. Assim, eventuais diferenças devem ser interpretadas como
evolução do trabalho, dentro das condições e limitações documentadas aqui.

Ao utilizar os resultados apresentados no capítulo, cite a publicação. Ao
utilizar o código, os dados ou as análises posteriores deste repositório, cite
também o repositório e informe a versão utilizada.

## Escopo de reprodutibilidade

Os arquivos-fonte recebidos não continham o *driver* que instanciou o GA e o
QGA e gravou os quatro arquivos `pickle`. Por isso, esta versão **não afirma
regenerar as otimizações completas do zero**. Os resultados das otimizações são
preservados em `data/`, com hashes SHA-256, e servem de entrada para as análises
reprodutíveis.

Esta distinção é importante:

- reproduzível: inspeção dos arquivos, simulações com os polos arquivados,
  métricas, figuras, análise de convergência e LMIs;
- verificável isoladamente: decodificação e execução determinística do QGA com
  semente fixa;
- não reconstruído: orquestrador original que executou todas as otimizações e
  gerou os `pickle`.

## Organização

```text
data/                  resultados precomputados e hashes
notebooks/             análise dos resultados e estabilidade por LMI
results/figures/       figuras finais selecionadas
scripts/               inspeção, validação e geração de artefatos
src/qga_maglev/        implementação do QGA e utilitários
tests/                 testes unitários e de reprodutibilidade
LICENSES/              licença e avisos de proveniência do QGA upstream
```

O backup idêntico do notebook, caches Python, a cópia local do pacote
`geneticalgorithm` e quatro figuras obsoletas não foram incluídos.

## Ambiente

A cópia publicada foi validada no seguinte ambiente:

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
- nbformat 5.10.4 e nbconvert 7.17.1.

Essas são as versões do ambiente usado para limpar e validar o repositório.
Nem todas estavam registradas nos artefatos históricos, portanto não devem ser
interpretadas como prova das versões usadas em cada execução original.

### Instalação no Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

### Instalação no Linux ou macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

## Configuração arquivada

Todos os arquivos de resultados registram semente global `42`, população de
`30` indivíduos e `50` gerações.

| Parâmetro | GA clássico | QGA |
|---|---:|---:|
| Semente | 42 | 42 |
| População | 30 | 30 |
| Gerações | 50 | 50 |
| Mutação | 0,15 | 0,01 por indivíduo; 0,001 por gene |
| Cruzamento | 0,70 | não se aplica |
| Elitismo | 0,05 | memória do melhor global |
| Bits por parâmetro | não se aplica | 10, 16, 24 ou 32 |
| Limiar de medição | não se aplica | 0,5 |

Os quatro parâmetros dos polos usam os limites `[5, 50]`, `[5, 50]`,
`[5, 50]` e `[1, 30]`. A função objetivo das otimizações usa uma simulação de
5 s; as simulações finais usam 10 s e passo de controle de 2 ms. Métricas
calculadas nesses dois horizontes não devem ser comparadas diretamente.

## Execução

Execute os comandos a seguir na raiz do repositório.

### 1. Verificar integridade e testes

A verificação de hashes não desserializa os arquivos `pickle`:

```powershell
python scripts/verify_data.py
python -m unittest discover -s tests -v
```

Teste curto e determinístico do QGA:

```powershell
python scripts/qga_smoke.py --seed 42
```

Esse teste usa uma função objetivo sintética; ele não representa uma nova
otimização da planta MAGLEV.

### 2. Inspecionar os resultados arquivados

```powershell
python scripts/inspect_results.py
```

O comando exibe sementes, configurações, ITAE e tempos registrados. Consulte o
aviso de segurança sobre `pickle` abaixo antes de executá-lo.

### 3. Reproduzir a análise e as figuras

```powershell
New-Item -ItemType Directory -Force results\notebooks | Out-Null
python -m nbconvert --to notebook --execute `
  notebooks\comparacao_eficiencia_qga_bits.ipynb `
  --output comparacao_eficiencia_qga_bits.executado.ipynb `
  --output-dir results\notebooks `
  --ExecutePreprocessor.timeout=-1
```

O notebook lê os quatro arquivos de `data/` e grava as figuras em
`results/figures/`. Seus arquivos versionados não contêm saídas incorporadas.

### 4. Executar a análise de estabilidade por LMI

```powershell
python -m nbconvert --to notebook --execute `
  notebooks\analise_estabilidade_lmi.ipynb `
  --output analise_estabilidade_lmi.executado.ipynb `
  --output-dir results\notebooks `
  --ExecutePreprocessor.timeout=-1
```

A análise verifica as malhas locais e busca uma matriz de Lyapunov quadrática
comum em janelas da faixa de operação. A viabilidade é numérica, depende da
formulação, da grade e do solver, e não constitui prova global fora das
condições testadas.

### 5. Regenerar a figura-resumo das métricas

```powershell
python scripts/regenerate_metrics.py `
  --output results\figures\comparacao_metricas_desempenho.png
```

Os valores desse gráfico são os valores finais de 10 s documentados no estudo,
e não os valores da função objetivo de 5 s.

### Comandos equivalentes para Linux ou macOS

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

## Valores de regressão

Alguns valores usados para conferir a análise final são:

| Configuração | ITAE final |
|---|---:|
| FT1 original | 1,6003e-3 |
| IT2-FLC original | 1,5819e-3 |
| FT1 + GA | 6,3559e-4 |
| IT2-FLC + GA | 6,0970e-4 |
| FT1 + QGA, 32 bits | 6,1251e-4 |
| IT2-FLC + QGA, 32 bits | 6,0509e-4 |

Tempos dependem do hardware e do ambiente. Tempos de convergência obtidos por
rateio são estimativas, não cronometragens de uma execução interrompida na
geração indicada.

## Segurança dos dados

Arquivos `pickle` podem executar código durante a desserialização. Carregue
somente os arquivos fornecidos neste repositório e confira antes os hashes com
`python scripts/verify_data.py`. Não use `inspect_results.py` ou os notebooks
para abrir arquivos `pickle` obtidos de terceiros não confiáveis.

## Licenças e atribuição

O código-fonte deste repositório é licenciado sob a licença MIT.
`src/qga_maglev/qga.py` contém trechos modificados derivados de
[ResearchCodesHub/QuantumGeneticAlgorithms](https://github.com/ResearchCodesHub/QuantumGeneticAlgorithms),
na revisão `d20ad57f0a2576a6c48d8c8c4f7870a6192275e8`. A implementação
upstream é atribuída a R. Lahoz-Beltra e distribuída sob a licença MIT,
Copyright (c) 2016 ResearchCodesHub. O cabeçalho histórico e a licença upstream
integral estão preservados em `LICENSES/QGA_UPSTREAM_NOTICE.txt` e
`LICENSES/ResearchCodesHub-QuantumGeneticAlgorithms-MIT.txt`. Consulte
[`THIRD_PARTY_NOTICES.pt-BR.md`](THIRD_PARTY_NOTICES.pt-BR.md) para detalhes da
atribuição e das modificações.

O backend GA clássico é o pacote externo `geneticalgorithm==1.0.2`, de Ryan
(Mohammad) Solgi, sob MIT. A cópia vendorizada não é necessária e foi removida.

Os dados arquivados e as figuras geradas são artefatos de pesquisa, não
software, e não são cobertos pela licença MIT do código. Eles são fornecidos
para verificação sob as declarações de direitos em `data/README.pt-BR.md` e
`results/README.pt-BR.md`; nenhuma licença aberta adicional para dados ou
conteúdo é concedida.

## Citação

Os metadados de citação estão em `CITATION.cff`. Ao reutilizar resultados, cite
também o capítulo de conferência associado e informe a resolução em bits, a
semente, a versão do repositório e o protocolo de comparação.

## Autoria

Israel da Silva Felix de Lima, 2026.
