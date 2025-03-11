import flet as ft

largura = 500

feedback = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white", 
    width=500,
    height=25,
    border_radius=10
)

def mudar_cor_feedback_campos(cor: str):
    if cor == "white":
        feedback.bgcolor = "white"
        feedback.content.value = ""
        feedback.update()
    if cor == "red":
        feedback.bgcolor = "red"
        feedback.content.value = "Campo(s) obrigatório(s) não preenchido(s)."
        feedback.update()


def criar_botao_sair(funcao):
    return ft.ElevatedButton(
        "Sair",
        on_click=funcao,
        color="white",
        bgcolor="#3254B4",
        icon="ARROW_BACK",
        icon_color="white",
        width=245
    )


def criar_botao_salvar(funcao):
    return ft.ElevatedButton(
        "Salvar e Sair", 
        on_click=funcao, 
        color="white",
        bgcolor="#3254B4",
        icon="SAVE",
        icon_color="white",
        width=245
    )