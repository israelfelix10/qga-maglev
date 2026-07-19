# Registro de validação

[English (US)](VALIDATION.md) | **Português (Brasil)**

Validação realizada em 18/07/2026, no ambiente descrito no
[`README.pt-BR.md`](README.pt-BR.md).

## Verificações concluídas

- Os quatro hashes SHA-256 de `data/SHA256SUMS` foram conferidos.
- Os seis testes unitários passaram.
- O teste curto do QGA produziu dez gerações com semente 42.
- A versão refatorada do QGA foi comparada à cópia original em um problema de
  regressão, usando a mesma semente, população, número de gerações, codificação
  e função objetivo. Parâmetros, melhor aptidão e histórico coincidiram
  exatamente.
- Após a atualização de licença e proveniência, a AST executável de `qga.py`
  permaneceu idêntica ao baseline validado; somente comentários e a docstring
  do módulo foram alterados.
- `notebooks/comparacao_eficiencia_qga_bits.ipynb` concluiu a execução integral
  por `nbconvert` e regenerou as figuras.
- `notebooks/analise_estabilidade_lmi.ipynb` concluiu a execução integral por
  `nbconvert` com CVXPY 1.9.1, Clarabel 0.11.1 e SCS 3.2.11.
- A busca textual não encontrou caminhos pessoais, credenciais, segredos
  expostos nem referências editoriais internas nos arquivos publicados.
- A proveniência do QGA foi conferida na revisão upstream
  `d20ad57f0a2576a6c48d8c8c4f7870a6192275e8`. A licença MIT upstream integral
  e o aviso histórico do código-fonte estão incluídos em `LICENSES/`.
- Um wheel foi construído com dependências de build isoladas, instalado em um
  destino temporário e usado no smoke test determinístico. Seus metadados
  registram `License-Expression: MIT`, e os cinco arquivos obrigatórios de
  licença e avisos de terceiros estão presentes em `dist-info/licenses/`.

## Limite da validação

As otimizações completas GA/QGA não foram repetidas. O conjunto de origem não
continha o *driver* que as executou e gravou os arquivos `pickle`. A validação
abrange os resultados arquivados, o pós-processamento, as simulações finais, as
figuras, as LMIs e o comportamento isolado do QGA.
