import os

CAMINHO_TABELA = os.path.join("articledb", "dados", "dados_tabela.txt")
CAMINHO_SINTESE = os.path.join("articledb", "dados", "dados_sintese.txt")

def obter_dados_tabela():
    """Obtem os dados da tabela da tela principal."""

    try:
        with open(CAMINHO_TABELA, mode="r") as arq:
            return [linha.split("\n")[0].split(",") for linha in arq.readlines()]

    except:
        with open(CAMINHO_TABELA, mode="x") as arq:
            return []


def atualizar_dados_tabela(dados_tabela:list):
    """Atualiza os dados que ja existem da tabela da tela principal."""

    with open(CAMINHO_TABELA, mode="w") as arq:
        arq.writelines([f"{linha}\n" for linha in dados_tabela])


def obter_dados_sintese():
    """Obtem os dados da tabela da tela principal."""

    try:
        with open(CAMINHO_SINTESE, mode="r") as arq:
            return eval(arq.read())
    except:
        with open(CAMINHO_SINTESE, mode="x") as arq:
            return {}


def atualizar_dados_sintese(dados_sintese:dict):
    """Atualiza os dados que ja existem da tela de sintese (pela tela principal, ao adicionar uma coluna de leitor nova)."""

    with open(CAMINHO_SINTESE, mode="w") as arq:
        arq.write(str(dados_sintese))