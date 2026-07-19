# Dados precomputados

[English (US)](README.md) | **Português (Brasil)**

Os quatro arquivos `pickle` contêm configurações, sementes, polos, históricos,
tempos e logs usados nas análises para 10, 16, 24 e 32 bits por parâmetro.

Antes de carregá-los, execute `python scripts/verify_data.py` na raiz do
repositório. O arquivo `SHA256SUMS` registra os hashes da cópia recebida. Como
`pickle` pode executar código durante a carga, não substitua estes arquivos por
cópias de origem desconhecida.

Os dados comuns do controlador original e do GA aparecem repetidos nos quatro
arquivos porque a estrutura histórica foi preservada para rastreabilidade.

## Proveniência e direitos

Estes arquivos são cópias fixas das saídas de otimização usadas na pesquisa
associada e foram fornecidos pelo autor do repositório a partir dos arquivos de
trabalho da pesquisa. Seus hashes são preservados para que análises posteriores
possam ser rastreadas até as mesmas entradas.

Os arquivos são dados de pesquisa, não software, e não são cobertos pela
licença MIT da raiz. Este repositório não concede uma licença aberta adicional
para os dados. O copyright e os direitos relacionados permanecem com seus
respectivos titulares. Os arquivos podem acompanhar este repositório para
verificação; obtenha autorização dos titulares antes de redistribuí-los,
modificá-los ou republicá-los.
