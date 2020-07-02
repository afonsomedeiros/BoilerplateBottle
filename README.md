# Boilerplate de projeto Bottle.

### Sobre o projeto.

O projeto "Boilerplate bottle" é uma estruturação de um projeto web utilizando o micro-framework Bottle. Pensado de modo a utilizar uma estrutura de apps que muito distantemente pode lembrar um pouco a estrutura o Django (mas óbviamente nem se compara).

### Como executar esse projeto.

Pode utilizar o "pipenv" para fazer a instalação das depêndencias (apenas o módulo bottle) ou utilizando o comando:

```sh
pip install bottle
```

Para executar o projeto basta utilizar o comando:

```sh
python server.py
```

### Criando uma action

Actions são os nomes que dei para funções no arquivo (ou módulo) action. Essa função precisa retornar uma String ou um template. Importando a classe Views do arquivo Views.py, pode retornar templates de dentro da pasta `templates`. A classe Views pode receber vários argumentos, os argumentos padrões são:

- app: De qual app deve ser procurado os templates.
- url: Identifica o agrupamento de templates.
- tpl: Identifica o template.

Na estrutura de diretórios:
```sh
app # diretório do app.
  - templates # diretório dos templates.
    - home # agrupamento de templates
      - index.html # template index.
    - about # agrupamento de templates.
      - about.html # template about.
```

Para retornar o template `/home/index.html` seria definido uma instancia de View da seguinte forma:

```py
from Views import Views


def index(*args, **kwargs):
  return Views()
```

O path `/app/template/home/index.html` é o path padrão portanto não é necessário passar nenhum argumento na instancia de Views. Agora para retornar o template `/about/about.html` é necessário retornar uma instancia da seguinte forma:

```py
from Views import Views


def index(*args):
  return Views(**kwargs)

def about(*args):
  return Views(url="about", tpl="about")
```

obs: Os parametros na função de certa forma são necessários em casos de utilização de url dinâmicas, vocês verão mais pra frente.

### Definindo rotas para as actions.

Depois de criar suas actions é necessário criar rotas para que essas actions sejam acessiveis. No arquivo `routes.py` tem uma função chamada `create_route(app)`, esta função é uma factory que "instala" as rotas num app. Para criar sua rota é necessário apenas usar a função route do parametro app da função.

```py
from bottle import Bottle
from . import actions


def create_route(app: Bottle):
  app.route('/', "GET", actions.index)
```

Desta forma criamos o endpoint "/" executando o projeto podemos acessar `http://localhost:8080/` e teremos o retorno do nosso template index. Dessa forma criamos endpoints para qualquer action que precisemos:

```py
from bottle import Bottle
from . import actions


def create_route(app: Bottle):
  app.route('/', "GET", actions.index)
  app.route('/about', "GET", actions.about)
```

### URLs dinâmicas.

Com a sintaxe acima depois dos testes que fiz não consegui definir de nenhuma forma uma url dinâmica, para definir uma url dinâmica precisamos utilizar a função `app.route()` como um decorador. Vamos criar uma action para poder testar.

```py
from Views import Views


def index(*args):
  return Views(**kwargs)

def about(*args):
  return Views(url="about", tpl="about")

def dinamica(teste):
  return f"Argumento passado pela url é {teste}"
```

Agora criaremos nosso endpoint utilizando a função `app.route()` como um decorador para outra função assim:

```py
from bottle import Bottle
from . import actions


def create_route(app: Bottle):
  app.route('/', "GET", actions.index)
  app.route('/about', "GET", actions.about)

  @app.route('/<teste>')
  def dinamica(teste):
    return actions.dinamica(teste)
```

Assim temos nossas URLs dinâmicas.

### Criando novos apps.

Eu tentei criar os apps seguindo um padrão que pudesse ser seguido em todos os apps. Portanto basta criar um diretório no mesmo nível do diretório app, adicionar a seguinte lista de arquivos:
- __init__.py
- routes.py
- actions.py (ou um módulo actions)

Vamos criar um app chamado `admin` para exemplificar.

Diretórios (apenas diretórios):
```sh
root
  admin
    templates
  app
    templates
  statics
```

Vamos aos arquivos:

```py
# /admin/__init__.py

from bottle import Bottle
from .routes import create_route


def create_admin():
    admin = Bottle()
    create_route(admin)
    return admin

# /admin/routes.py

from bottle import Bottle


def create_route(app: Bottle):
    @app.route("/")
    def teste():
        return "App admin"
```

Não criaremos os outros arquivos, para fins de explicação apenas estes bastão, mas no seu projeto crie o módulo completo. Agora precisamos adicionar algumas linhas no arquivo `server.py`.

```py
# server.py
from app import create_app
from settings import ROOT_PATH
from bottle import static_file

from admin import create_admin # adicionado factory do novo app.


app = create_app()
app.mount('/admin', create_admin()) # Criada gestão de rotas do novo app.


@app.get("/statics/<path:path>")
def statics(path):
    return static_file(path, root=f"{ROOT_PATH}/statics/")


@app.get("/favicon.ico")
def favicon():
    return static_file("favicon.png", root=f"{ROOT_PATH}/statics/img/favicon/")


if __name__ == '__main__':
    app.run(debug=True, reloader=True)
```

Pronto, agora podemos criar nossas rotas no app admin e qualquer rota deve iniciar com `/admin/` para poder ser acessada.

TODO
- [x] Criar documentação do proejto.
- [x] Explicar como utilizar os `actions.py`.
- [x] Explicar como criar rotas.
- [x] Explicar como criar novos apps.
