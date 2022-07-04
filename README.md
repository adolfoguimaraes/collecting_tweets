# Coleta de Tweets utilizando o TWARC

Esse repositório possui scripts em python para realizar a coleta de tweets utilizando a biblioteca [TWARC](https://twarc-project.readthedocs.io/en/latest/). A biblioteca permite utilizar a versão mais nova da API do Twitter (v2), além de ter acesso aos recursos para quem tem o _Academic Access Research_. 

Foram implementos scripts para três funcionalidades: 

Os scripts de busca estão implementados na pasta `scripts/`. Na pasta `examples` existem exemplos de uso de cada um dos scripts. 

**Stream**

Busca em tempo real do tweets a partir de um conjunto de strings de consultas. 

O método `stream` recebe os seguintes parâmetros: 

* `seach_rules`: lista com as string de buscas que serão pesquisadas;
* `id`: string de identificação da busca. Será associado ao arquivo resultado da busca.
* `limit`: número de tweets que serão retornados. Existe uma limitação mensal de acordo com o tipo de conta que você tem na API. 
* `folder`: local que o arquivo de saída será armazendo.

O método retorna como saída um arquivo do timpo JSONL (json lines, onde cada linha é um json válido) com o nome `id`.jsonl na pasta `folder`.

Essa busca é encerrada quando o valor de `limit` é atingido ou apertando `Crlt + C`.

_Exemplo_

```python
from scripts.collect import Collect

c = Collect("config.ini")

c.stream(
    search_rules=["sergipe OR bahia", "brasil"], 
    limit=20, 
    folder="coleta/teste1", 
    id="coletabrasil1"
)
```

**Recent Search**

Busca dos tweets mais recentes a partir de uma string de busca.

O método `search` recebe os seguintes parâmetros: 

**Archive Search**

Busca de tweets a partir de uma data específica. Esse recurso é exclusivo para quem tem acesso ao _Academic Access Research_. Ele permite a busca nos arquivos de todo histórico do twitter desde de 21/03/2006.

O método `search_archive` recebe os seguintes parâmetros: 






