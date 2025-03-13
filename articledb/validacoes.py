import flet as ft
import re
import datetime

# Padrões de regex
FILTRO_TITULO = r"^[a-zA-Z0-9áéíóúÁÉÍÓÚâêôÂÊÔçÇ\s\-]*$"
FILTRO_LINK = r"^[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]*$"
FILTRO_AUTORES = r"^[A-ZÁÉÍÓÚÂÊÔÇ\s,\.;]*$"
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


def validar_input(valor: str, campo: str) -> bool:
    valor = str(valor).strip()
    campo = str(campo)

    match campo:
        case "Título":
            # Mínimo: 3. Escolha arbitrária.
            # Máximo: 400. Escolha arbitrária.

            if not (3 <= len(valor) <= 400):
                return False

        case "Link":
            # Mínimo: 11. Menor URL válida: http://a.bc
            # Máximo: 2000. Recomendação do Google: https://support.google.com/webmasters/thread/278099742?hl=en&msgid=278133107
            if not (11 <= len(valor) <= 2000):
                return False
            
            padrao_link = ''.join(
                (
                    r"https?://",                           # Protocolo http:// ou https://
                    r"(?=[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+)",  # Deve haver pelo menos um ponto entre domínios
                    r"(?!.*[\.\?\#&=%]$)",                  # Não pode terminar com caracteres especiais de URL
                )
            )

            if not re.fullmatch(padrao_link, valor):
                return False


        case "Autores":
            # Mínimo: 5. Menor autor válido: A, B.
            # Máximo: 400. Escolha arbitrária
            if not (5 <= len(valor) <= 400):
                return False
            
            autores = valor.split(';') if ';' in valor else [valor]

            padrao_autores = r"[A-Z]+\s[A-Z]\." # 'SOBRENOME, N.' (N = Nome)

            if not all(re.fullmatch(padrao_autores, autor) for autor in autores):
                return False
            

        case "Ano":
            # Mínimo: 1665. Periódico mais antigo da história: Journal des Sçavans.
            # Máximo: Ano atual.
            if not (1665 <= int(valor) <= datetime.datetime.now().year):
                return False
            

        case "Local de Publicação":
            pass


        case "Abstracts":
            pass


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