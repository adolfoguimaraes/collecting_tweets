# Coleta de Tweets utilizando o TWARC

Esse repositório possui scripts em python para realizar a coleta de tweets utilizando a biblioteca [TWARC](https://twarc-project.readthedocs.io/en/latest/). A biblioteca permite utilizar a versão mais nova da API do Twitter (v2), além de ter acesso aos recursos para quem tem o _Academic Access Research_. 

Os scripts de busca estão implementados na pasta `scripts/`. Na pasta `examples` existem exemplos de uso de cada um dos scripts. 

Foram implementos scripts para três funcionalidades: 

## Acesso à API do Twitter

Para executar os scripts é necessário ter uma conta de desenvolvedor no Twitter. O cadastro de desenvolvedor pode ser feito no link: https://developer.twitter.com/.

A configuração para executar os scripts é feito a partir do arquivo `config.ini`. Para isso, renomei o arquivo `config.ini.example` para `config.ini` e preencha o campo adequado com a chave de desenvolvedor. O Bearer Token pode ser gerado diretamente no portal de desenvolvedor. Essa chave é necessária para conectar à versão 2.0 da API do Twitter.

_Modelo do arquivo de configuração_

```ini
[TWITTER]

BEARER_TOKEN = COLOQUE SUA CHAVE AQUI.
```

Alguns acessos só é permitido para os usuários que tem _Academic Research Access_. Mais detalhes dos requisitos para solicitar esse tipo de acesso está disponível no link: https://developer.twitter.com/en/products/twitter-api/academic-research. 

## Funcionalidades

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

* `query`: string de busca que será pesquisada no twitter;
* `id`: string de identificação da busca. Será associado ao arquivo resultado da busca.
* `limit_pages`: número de páginas que serão retornadas na busca. Cada página tem no máximo `max_per_request` tweets. O número máximo de tweets que podem ser retornado por página é 100. A primeira página possui os tweets mais recentes. 
* `max_per_request`: máximo de tweets que serão retornados por página. Esse valor é limitado a 100. 
* `folder`: local que o arquivo de saída será armazendo.

O método retorna como saída um arquivo JSONL (json lines, onde cada linha é um json válido) para cada página coletada  com o nome `[ID]_page[NUMERODAPAGINA]`.jsonl na pasta `folder`. O método é finalizado quando atingir o número limite de páginas solicitadas.

_Exemplo_

```python
from scripts.collect import Collect

c = Collect("config.ini")

c.search(
    "brasil", 
    limit_pages=1, 
    max_per_request=10, 
    folder="coleta/teste1", 
    id="coletabrasil1"
)
```

**Archive Search**

Busca de tweets a partir de uma data específica. Esse recurso é exclusivo para quem tem acesso ao _Academic Access Research_. Ele permite a busca nos arquivos de todo histórico do twitter desde de 21/03/2006.

O método `search_archive` recebe os seguintes parâmetros: 

* `query`: string de busca que será pesquisada no twitter;
* `id`: string de identificação da busca. Será associado ao arquivo resultado da busca.
* `max_per_request`: máximo de tweets que serão retornados por página. Esse valor é limitado a 100. 
* `folder`: local que o arquivo de saída será armazendo.
* `time`: esse parâmetro é um dicionário que define a data que os tweets serão consultados. O dicionario tem as seguintes chaves:
    * `end`: data final da busca.
    * `delta`: esse parâmetro define a data início de busca. Por exemplo, se o `end` é 01/07/2022 22:00, um delta de 1 hora mais definir a data inicial de busca para 01/07/2022 21:00.
    * `delta_type`: define a métrica do delta. Esse valor pode assumir `hour` ou `minute`.

O método retorna como saída um arquivo do tipo JSONL (json lines, onde cada linha é um json válido). Os arquivos serão salvos na pasta `folder`. Como essa busca pode coletar muitos tweets. Eles serão salvos em diferentes arquivos de acordo com a granularidade (hora ou minuto passado no atributo `delta_type`) escolhida e a página retornada. com o nome `[id]_[INT]_page[NUMERODAPAGINA]`.jsonl na pasta `folder`.

`INT` indica um contador dentro da granularidade. Por exemplo, se a granularidade for de 1 hora, esse valor vai ser 0 na primeira hora coletada, 1 na segunda, 2 na terceira e assim por diante. Dentro de cada hora, o número da página é reiniciado. 

_Exemplo_

```python
from scripts.collect import Collect
import datetime


c = Collect("config.ini")

time = {
    "end": datetime.datetime.strptime("2022-07-02 23:59:59", "%Y-%m-%d %H:%M:%S"), 
    "delta": 5, 
    "delta_type": "minute"
}

c.search_archive(
    "brasil OR sergipe", 
    max_per_request=100, 
    time=time, 
    id="coletabrasil2", 
    folder="coleta/teste1"
)

```
