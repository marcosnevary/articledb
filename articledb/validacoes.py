import re

#--------------------------------------------------------------------- FUNCAO PESQUISA TELA PRINCIPAL -----------------------------------------------------------
def achar_nome_tela_principal(string:str, artigo:list)->list:
    string = string.lower()

    #verificando cada item da linha, menos os botoes de leitor
    for celula in artigo[:6]:
        if re.match(string, celula.lower()): #retornando true se der match
            return True

    #retornando false se nada der match
    return False






