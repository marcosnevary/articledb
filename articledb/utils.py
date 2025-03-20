import flet as ft

largura = 600
regex_string = r"^[a-zA-ZÃÁÀÂãàáâÊÁÈêéèÍÎÌîíìÓÔÒÕóôòõÚÛÙúûùç\s]*$"


def criar_botao_sair(funcao, texto):
    return ft.ElevatedButton(
        text=texto,
        on_click=funcao,
        color="white",
        bgcolor="#3254B4",
        icon="ARROW_BACK",
        icon_color="white",
        width=245
    )


def criar_botao_salvar(funcao, texto):
    return ft.ElevatedButton(
        text=texto,
        on_click=funcao,
        color="white",
        bgcolor="#3254B4",
        icon="SAVE",
        icon_color="white",
        width=245
    )
