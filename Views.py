from bottle import template
from settings import ROOT_PATH


class Views:
    """Classe que lida e direciona os templates.
       @param __path: diretorios do projeto em questao."""

    def __new__(cls, app="app", url='home', tpl='index', **kwargs):
        """
        Construtor da classe Views.
        @app: Nome do app onde serão procurados os templates.
        @url: Nome do controlador e tambem da pasta que faz a divisao dos
        servicos.
        Valor padrao: Home
        EX:
            Controlador: Home.
                Pasta Templates -> Pasta Home
            Controlador: Cadastros
                Pasta Templates -> Pasta Cadastros
        @tpl: Nome do template da pagina, deve ser o mesmo nome do arquivo html
        da pagina.
        Valor padrao: index
        EX:
            Controlador: home -> portanto url = Home
            Template: index -> portanto tpl = index
            rota: '/home/index'
            caminho completo: '{ROOT_PATH}/{app}/templates/home/index.html
        @kwargs: Parametros passados para as paginas na renderizacao dos
        templates.

        Chave do dicionário ARGS: TEMPLATE_BASE_LAYOUT
            Esta chave contem diretorio do layout. O layout pode ser modificado
            e pode ser movido para
            outro diretorio, apenas nao esqueca de atualizar a chave
            'TEMPLATE_BASE_LAYOUT' para poder
            localizar o novo local/arquivo de layout.

            OBS: continua sendo perfeitamente possivel referenciar o arquivo
            diretamente no template.
        """
        cls.__path = f"{ROOT_PATH}/{app}/templates"
        cls.args = kwargs
        cls.args['TEMPLATE_BASE_LAYOUT'] = f"{cls.__path}/base.html"

        if tpl and url:
            return template(f"{cls.__path}/{url}/{tpl}.html",
                            cls.args)
