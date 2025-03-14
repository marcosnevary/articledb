from time import sleep

import flet as ft

from articledb import controle

# GERAL

def atualizar_feedback_leitor(cor, msg):
    feedback_leitor.bgcolor = cor
    feedback_leitor.content.value = msg
    if feedback_leitor.page:
        feedback_leitor.update()


feedback_leitor = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white",
    width=250,
    height=25,
    border_radius=10
)


def atualizar_feedback(msg, cor):
    txt_mensagem_feedback.value = msg
    container_mensagem_feedback.bgcolor = cor

    controle.pagina.update()

    #voltando a cor e texto ao original
    sleep(10)
    txt_mensagem_feedback.value = ""
    container_mensagem_feedback.bgcolor = "white"

    controle.pagina.update()


txt_mensagem_feedback = ft.Text(value = "", expand=True, color=ft.colors.WHITE)


container_mensagem_feedback = ft.Container(
    content=txt_mensagem_feedback,
    bgcolor=ft.colors.WHITE,
    width=2000,
    expand=True,
    alignment=ft.alignment.center,
    height=25,
    border_radius=10
)


# TELA DE CADASTRO
# TELA DE EDIÇÃO
# TELA DE SÍNTESE
feedback_registro = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white",
    width=500,
    height=25,
    border_radius=10,
)


def atualizar_feedback_registro(cor, msg):
    feedback_registro.bgcolor = cor
    feedback_registro.content.value = msg
    if feedback_registro.page:
        feedback_registro.update()