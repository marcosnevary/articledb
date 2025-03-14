import os

CAMINHO_TABELA = os.path.join("dados", "dados_tabela.txt")
CAMINHO_SINTESE = os.path.join("dados", "dados_sintese.txt")


def obter_dados_tabela() -> list[list[str]] | list:
    """
    Obtém os dados da tabela da tela principal.

    Diretório esperado: `articledb/dados/dados_tabela.txt`

    Returns:
        list[list[str]]: Lista de listas de string com dados da tabela, caso o arquivo exista.

        Se o arquivo não existir, retorna uma lista vazia.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """

    try:
        with open(CAMINHO_TABELA, mode="r", encoding="UTF-8") as arq:
            conteudo = arq.readlines()

            if not conteudo:
                return []

            return [linha.strip().split("|") for linha in conteudo]

    except:
        with open(CAMINHO_TABELA, mode="x", encoding="UTF-8") as arq:
            return []


def atualizar_dados_tabela(dados_tabela: list) -> None:
    """
    Atualiza os dados que já existem na tabela da tela principal.

    Diretório esperado: `articledb/dados/dados_tabela.txt`

    Args:
        dados_tabela (list[str]): Lista de strings representando os dados da tabela.
            
            Cada elemento da lista é uma linha do arquivo.
    """

    with open(CAMINHO_TABELA, mode="w", encoding="UTF-8") as arq:
        arq.writelines([f"{linha}\n" for linha in dados_tabela])


def obter_dados_sintese() -> dict:
    """
    Obtém os dados da tabela da tela de síntese.

    Diretório esperado: `articledb/dados/dados_sintese.txt`

    Returns:
        conteudo (dict): Dicionário de dicionários com dados de síntese, caso o arquivo exista.

            Se o arquivo não existir ou a tabela estiver vazia, retorna um dicionário vazio.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """

    try:
        with open(CAMINHO_SINTESE, mode="r", encoding="utf-8") as arq:
            conteudo = arq.read()

            if not conteudo:
                return {}

            return eval(conteudo)
       
    except:
        with open(CAMINHO_SINTESE, mode="w") as arq:
            return {}


def atualizar_dados_sintese(dados_sintese: dict) -> None:
    """
    Atualiza os dados que já existem na tabela da tela de síntese.

    Diretório esperado: `articledb/dados/dados_sintese.txt`

    Args:
        dados_tabela (dict): Dicionário de dicionários representando os dados da tabela.
            
            As chaves do dicionário externo são leitores.
            
            As chaves do dicionário interno são campos de síntese.
    """

    with open(CAMINHO_SINTESE, mode="w", encoding="utf-8") as arq:
        arq.write(str(dados_sintese))
