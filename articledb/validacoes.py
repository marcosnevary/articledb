import re

def tratar_string(string:str):
    string = string.lower()
    string = re.sub(r"[ãàáâ]", "a", string)
    string = re.sub(r"[êéè]", "e", string)
    string = re.sub(r"[îíì]", "i", string)
    string = re.sub(r"[óôòõ]", "o", string)
    string = re.sub(r"[úûù]", "u", string)
    string = re.sub(r"[ç]", "c", string)
    return string


def achar_nome_tela_principal(string:str, artigo:list)->list:
    string = tratar_string(string)

    for celula in artigo[:6]:
        texto = tratar_string(celula)
        if re.match(string, texto): #retornando true se der match
            return True
    
    return False #retornando false se nada der match