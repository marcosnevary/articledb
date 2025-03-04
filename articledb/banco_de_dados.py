import controle

#-------------------------------------------------------------- FUNCOES DADOS DA TABELA ------------------------------------------------------------------------------

def carregando_dados_tabela():
    """Essa funcao vai carregar os dados da tabela da tela principal"""

    try: #ARQUIVO JA EXISTE, RETORNANDO A LISTA PRA TELA
        with open(r"articledb\dados\dados_tabela.txt", mode="r") as arq:
            return [linha.split("\n")[0].split(",") for linha in arq.readlines()]

    except: #ARQUIVO NAO EXISTE, CRIANDO ARQUIVO E RETORNANDO LISTA VAZIA
        with open(r"articledb\dados\dados_tabela.txt", mode="x") as arq:
            return []



def atualizando_dados_tabela(dados_tabela:list):
    """Essa funcao vai atualizar os dados que ja existem da tabela da tela principal"""
    
    try: #ARQUIVO JA EXISTE, SALVANDO TUDO
        with open(r"articledb\dados\dados_tabela.txt", mode="w") as arq:
            arq.writelines([f"{linha}\n" for linha in dados_tabela])

    except: #ARQUIVO NAO EXISTE, CRIANDO ARQUIVO E SALVANDO
        with open(r"articledb\dados\dados_tabela.txt", mode="x") as arq:
            pass



#-------------------------------------------------------------- FUNCOES DADOS DA SINTESE -----------------------------------------------------------------------------

def carregando_dados_sintese():
    """Essa funcao vai carregar os dados da tabela da tela principal"""

    try: #ARQUIVO JA EXISTE, RETORNANDO O DICIONARIO DO ARQUIVO
        with open(r"articledb\dados\dados_sintese.txt", mode="r") as arq:
            return eval(arq.read())

    except: #ARQUIVO NAO EXISTE, CRIANDO ARQUIVO E RETORNANDO DICIONARIO VAZIO
        with open(r"articledb\dados\dados_sintese.txt", mode="x") as arq:
            return dict()


def atualizando_dados_sinteses(dados_sintese:dict):
    """Essa funcao vai atualizar os dados que ja existem da tela de sintese (pela tela principal, ao adicionar uma coluna de leitor nova)"""
    
    try: #ARQUIVO JA EXISTE, SALVANDO TUDO
        with open(r"articledb\dados\dados_sintese.txt", mode="w") as arq:
            arq.write(str(dados_sintese))

    except: #ARQUIVO NAO EXISTE, CRIANDO ARQUIVO E SALVANDO
        with open(r"articledb\dados\dados_sintese.txt", mode="x") as arq:
            pass



