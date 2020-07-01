[![Build Status](https://api.cirrus-ci.com/github/cavalcantigor/flaskeleton-api.svg)](https://cirrus-ci.com/github/cavalcantigor/flaskeleton-api)
[![codecov](https://codecov.io/gh/cavalcantigor/flaskeleton-api/branch/master/graph/badge.svg)](https://codecov.io/gh/cavalcantigor/flaskeleton-api)
## Flaskeleton API
> Uma aplicação minimalista e completamente funcional contemplando todas as características de uma API
> completa utilizando *Flask*, *SQLAlchemy*, *Flask-Migrate*, *Marshmallow* e *APIBlueprint*. Pode
> ser facilmente configurada e ajustada conforme necessidades,
> muito útil em cenários de PoC's (proof of concept).

#### Setup inicial
Recomendamos utilizar um ambiente virtual `python` para execução
do projeto. Problemas com o *SQLAlchemy* e conflitos entre
pacotes ocorrem facilmente quando utilizado num único ambiente
com outros projeto `python`.

Portanto, indicamos a utilização do [*VirtualEnvWrapper*](https://virtualenvwrapper.readthedocs.io/en/latest/)
para isolar a instalação dos pacotes em `requirements.txt`.

Caso não esteja interessado em utilizar um ambiente virtual python,
também tem a opção de rodar num *container docker*. Recomendamos
a instalação do [*docker-compose*](https://docs.docker.com/compose/), o qual já está integrado
com este projeto.

Com o *docker-compose* já instalado, execute
```shell script
docker-compose up -d
``` 
para subir o *container* e iniciar a aplicação e
```shell script
docker-compose down
```  
para matar o *container* e encerrar a aplicação.

Para auxiliar no processo de deploy, debug e testes, o arquivo `Makefile`
contém alguns comandos úteis que podem ser acessados através de 
```shell script
make help
```

#### Estrutura do projeto
A aplicação consiste em um pacote principal `app` que contém toda a aplicação.
Dentro do pacote principal são encontrados pacotes das camadas de controle,
modelo, visualização (*endpoints*), acesso aos dados e um
modulo comum com ferramental útil.

    |-- app
    |   | -- commons
    |   | -- controllers
    |   | -- dao
    |   | -- models
    |   | -- resources
    |   | -- templates
    | -- config
    | -- docs
    | -- migrations
    | -- tests

Além dos pacotes principais, pacotes como `docs` e `templates` são
auxiliares e utilizados pela *API Blueprint*, além do pacote `migrations`
utilizado pela extensão *Flask-Migrate*.

#### Configurações
Esse projeto utiliza o [dynaconf](https://github.com/rochacbruno/dynaconf/)
para gerenciar suas configurações. Um arquivo [settings](/config/settings.toml)
na pasta `config` contém as configurações que devem ser 
carregadas de acordo com o ambiente que a aplicação está
rodando, conforme recomendado em 
[12 factor](https://12factor.net/).

Uma variável de ambiente `ENV_FOR_DYNACONF` contém
a configuração a ser carregada. Por exemplo, para os 
testes, deve ser executado da seguinte maneira
```shell script
ENV_FOR_DYNACONF=testing pytest -rpf
```

A única peculiaridade das configurações é o fato de
estar utilizando a extensão `dynaconf` para `Flask` 
([flask-extension](https://dynaconf.readthedocs.io/en/2.2.3/guides/flask.html)),
que injeta configurações de ambiente nas configurações
da aplicação que podem ser acessadas via `app.config`.
Além de facilitar o desenvolvimento, facilita a integração
de configurações utilizando uma única lib. Para alterar, 
via variável de ambiente, uma configuração do `flask`,
como, por exemplo, a *string* de conexão utilizada pelo
`SQLAlchemy`, deve-se utilizar:
```shell script
export FLASK_SQLALCHEMY_DATABASE_URI='minhastringdeconexao'
```
Atenção ao prefixo `FLASK_`, que deve ser utilizado. 
Isso pode ser alterado também.

Fique à vontade para livremente excluir, alterar e 
incluir configurações.

#### Flask-Migrate
A aplicação é completamente funcional e autocontida, ou seja, funciona
sem dependências externas. Para auxiliar nesse processo foi utilizado
juntamente com o ORM *SQLAlchemy* a extensão [*Flask-Migrate*](https://flask-migrate.readthedocs.io/en/latest/). É
ela a responsável por construir a base de dados, migrar alterações
e manter a consistência dos dados. Para tanto, é necessário efetuar,
antes de iniciar a aplicação, a construção da base de dados.

A base de dados, nessa aplicação, é mantida utilizando o [*SQLite3*](https://www.sqlite.org/index.html). Portanto,
antes de executar a aplicação, certifique-se de que está rodando corretamente
em sua máquina. O *SQLite3* é uma excelente escolha para uma aplicação pequena,
como essa, que serve de exemplo para uso do ORM e principais funcionalidades
do framework *Flask*. Isso pode ser alterado no arquivo
de configurações, bastando alterar a string de conexão
para o banco de sua escolha.

Ao executar pela primeira vez, rode o comando 
```shell script
flask db migrate
```
para garantir a criação de tabelas e gerar um `script` de revisão
que levará quaisquer mudanças nos seus `models` para suas tabelas.

Em seguida, execute
```shell script
flask db upgrade
```
para de fato atualizar as tabelas da base de dados.

Ao concluir com sucesso pela primeira vez os comandos acima,
note a criação de um arquivo chamado `flaskeleton.db`. Esse
é o banco de dados *SQLite3* da aplicação.

Caso suba a aplicação em *docker container*, um comando no
Makefile está disponível para criação das tabelas dentro
da base de dados no container.
```shell script
make container-create-db
```

#### Multi-Tenant
Para solucionar um problema específico de domínio de problema,
a API foi criada para responder requisições multicontexto.
Ou seja, a mesma requisição pode carregar um contexto no cabeçalho
da requisição para apontar qual banco de dados deseja utilizar
(*multi-tenant*).

Para não haver problemas com o funcionamento do *SQLAlchemy*
e o *script* de *migrate*, existe nas configurações a variável
`SQLALCHEMY_DATABASE_URI` que determina a base de dados *default*,
ou seja, aquela que irá ser criada por padrão. Há ainda
a variável `SQLALCHEMY_BINDS` que contém os mapeamentos disponíveis
(nesse caso, `production` é ilustrativo e aponta para uma
base de dados inexistente). A variável `DEFAULT_TENANT` 
é responsável por indicar qual o `bind` padrão em caso de não
fornecimento via cabeçalho do `bind` a ser utilizado. Por fim,
o *multi-tenant* pode ser desabilitado por meio da variável
`ENABLE_MULTI_TENANT`.

Todas as variáveis podem ser livremente configuradas de acordo
com a necessidade do desenvolvedor, inclusive desabilitando
o recurso de multicontexto.

> Tip: pode-se criar uma cópia do arquivo `flaskeleton.db` criado
> no passo anterior e renomeá-lo para `production.db` para
> testar o funcionamento do multi-contexto (lembre-se de passar
> o contexto no cabeçalho por meio de `Context` para alternar
> entre os `binds`).

#### Documentação da API

Para acessar a documentação da API, acesse a seguinte rota:

```
http://127.0.0.1:{PORTA}/flaskeleton-api/apidocs/
```

A API possui um arquivo de documentação *default* utilizando a especificação do *[Blueprint](https://apiblueprint.org/)*.
O arquivo está em: `./docs/api-blueprint-sample.apib`.

Preferimos deixar a responsabilidade da renderização do template HTML para o desenvolvedor.
Sempre que houver atualizações na especificação de endpoints da sua API, será de responsabilidade do desenvolvedor 
realizar a atualização e renderização do documento estático.
Para isso, basta utilizar as ferramentas existentes e sugeridas pelo *[Blueprint](https://apiblueprint.org/)*.

Afim de facilitar o processo de gerar o HTML, descrevemos ele a seguir.

##### 1. Instale o *Render*

Uma das ferramentas sugeridas pelo *Blueprint* é o [Aglio](https://github.com/danielgtaylor/aglio).
Usaremos ele:

```npm install -g aglio```

##### 2. Gere a documentação.

Para isso, entre na raíz do projeto e execute o seguinte comando:

```
aglio -i ./docs/api-blueprint-sample.apib --theme-full-width --no-theme-condense -o ./app/templates/apidocs/index.html
```

O Output será um arquivo ```index.html``` dentro de ```./app/templates/apidocs/index.html```
que é servido através do endpoint da aplicação.

*p.s: O arquivo base para esta documentação foi retirado de: [Definindo APIs com o API Blueprint](https://eltonminetto.net/post/2017-06-29-definindo-apis-com-api-blueprint/)*.
