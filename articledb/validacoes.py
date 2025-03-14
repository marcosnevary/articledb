import flet as ft
import re
import datetime

# Padrões de regex
FILTRO_TITULO = r"^[a-zA-Z0-9áéíóúÁÉÍÓÚâêôÂÊÔçÇ\s\-\.,;:!?&]*$"
FILTRO_LINK = r"^[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]*$"
FILTRO_AUTORES = r"^[a-zA-ZáéíóúÁÉÍÓÚâêôÂÊÔçÇ\s,\.;]*$"
FILTRO_ANO = r"^[0-9]*$"
FILTRO_LOCAL = r"^[a-zA-Z0-9áéíóúÁÉÍÓÚâêôÂÊÔçÇ\s\-]*$"
FILTRO_ABSTRACTS = r"^[a-zA-Z0-9áéíóúÁÉÍÓÚâêôÂÊÔçÇ\s\-]*$"


# Dicionário de filtro
componente_filtro = {
    "Título": ft.InputFilter(regex_string=FILTRO_TITULO, allow=True, replacement_string=""),
    "Link": ft.InputFilter(regex_string=FILTRO_LINK, allow=True, replacement_string=""),
    "Autores": ft.InputFilter(regex_string=FILTRO_AUTORES, allow=True, replacement_string=""),
    "Ano": ft.InputFilter(regex_string=FILTRO_ANO, allow=True, replacement_string=""),
    "Local de Publicação": ft.InputFilter(regex_string=FILTRO_LOCAL, allow=True, replacement_string=""),
    "Abstracts": ft.InputFilter(regex_string=FILTRO_ABSTRACTS, allow=True, replacement_string=""),
}

def validar_titulo(titulo: str) -> bool:
    """
    Valida o campo de título.

    Mínimo: 3. Escolha arbitrária.

    Máximo: 350. O maior título de artigo do mundo tem 345: 
    http://gomerpedia.org/wiki/What_is_the_longest_journal_article_title_in_the_literature%3F

    Args:
        valor (str): Valor no campo "Título".

    Returns:
        bool: Verdadeiro se cumprir os requisitos. Falso caso contrário.
    """

    titulo = str(titulo).strip()

    if not (3 <= len(titulo) <= 350):
        return False
    

    if not re.fullmatch(FILTRO_TITULO, titulo):
        return False
    
    return True


def validar_link(link: str) -> bool:
    """
    Valida o campo de link.

    Mínimo: 11. Menor URL válida: "http://a.bc"

    Máximo: 2000. Recomendação do Google: 
    https://support.google.com/webmasters/thread/278099742?hl=en&msgid=278133107
    
    Args:
        valor (str): Valor no campo "Link".

    Returns:
        bool: Verdadeiro se cumprir os requisitos. Falso caso contrário.
    """
    link = str(link).strip()

    if not (11 <= len(link) <= 2000):
        return False
    
    padrao_link = ''.join(
        (
            r"https?://",                                   #  Protocolo http ou https
            r"(?=[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+)",          #  Deve haver pelo menos um ponto entre domínios
            r"(?!.*[\?\#&=%@_\-]$)",                        #  Não pode terminar com certos caracteres na URL
            r"[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]{4,}"    #  4 caracteres (permitidos) ou mais no resto da URL
        )
    )

    if not re.fullmatch(padrao_link, link):
        return False
    
    return True


def validar_autores(autores: str) -> bool:
    """
    Valida o campo de autores.

    Mínimo: 5. Menor autor válido: "A, B."

    Máximo: 400. Escolha arbitrária
    
    Args:
        valor (str): Valor no campo "Autores".

    Returns:
        bool: Verdadeiro se cumprir os requisitos. Falso caso contrário.
    """
    autores = str(autores).strip()

    if not (5 <= len(autores) <= 400):
        return False
            
    autores = autores.split(';') if ';' in autores else [autores]

    padrao_autores = r"[A-Z]+,\s[A-Z]\." # "SOBRENOME, N." (N = Nome)

    if not all(re.fullmatch(padrao_autores, autor) for autor in autores):
        return False
    
    return True

def validar_ano(ano: str) -> bool:
    """
    Valida o campo de ano.

    Dígitos: 4.

    Número mínimo: 1665. Periódico mais antigo da história: Journal des Sçavans.

    Máximo: Ano atual.
    
    Args:
        valor (str): Valor no campo "Ano".

    Returns:
        bool: Verdadeiro se cumprir os requisitos. Falso caso contrário.
    """
    ano = str(ano).strip()

    if len(ano) != 4:
        return False

    try:
        ano_num = int(ano)

    except ValueError:
        return False

    if not (1665 <= ano_num <= datetime.datetime.now().year):
        return False
    
    return True


def validar_local(local: str) -> bool:
    """
    Valida o campo de local de publicação.

    Mínimo: 2. 
    Referência: https://en.wikipedia.org/wiki/List_of_short_place_names#:~:text=Bo%2C%20a%20city%20in%20Sierra%20Leone

    Máximo: 22. 
    Referência: https://en.wikipedia.org/wiki/List_of_long_place_names#:~:text=Parangaricutirimicuaro,Juan%2C%20and%20Parangaricutiro.
    
    Args:
        valor (str): Valor no campo "Local de Publicação".

    Returns:
        bool: Verdadeiro se cumprir os requisitos. Falso caso contrário.
    """
    local = str(local).strip()

    if not (2 <= len(local) <= 22):
        return False
    
    if not re.fullmatch(FILTRO_LOCAL, local):
        return False
    
    return True


def validar_abstracts(abstracts: str) -> bool:
    """
    Valida o campo de abstracts.

    Mínimo: 1. Escolha arbitrária.

    Máximo: 2000. Escolha arbitrária.

    Args:
        valor (str): Valor no campo "Abstracts".

    Returns:
        bool: Verdadeiro se cumprir os requisitos. Falso caso contrário.
    """
    abstracts = str(abstracts).strip()

    if not (1 <= len(abstracts) <= 2000):
        return False
    
    if not re.fullmatch(FILTRO_ABSTRACTS, abstracts):
        return False
    
    return True


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