import flet as ft
import controle
import banco_de_dados as bd
import tela_principal
import os
from utils import largura, criar_botao_sair, criar_botao_salvar

CAMINHO_SINTESE = os.path.join("articledb", "imagens", "sintese.png")

rotulo_componente = {
    "Objetivo": "objetivo",
    "Contribuições": "contribuicoes",
    "Lacunas Encontradas": "lacunas",
    "Observações": "observacoes"
}

componentes = {
    "objetivo": ft.Ref[ft.TextField](),
    "contribuicoes": ft.Ref[ft.TextField](),
    "lacunas": ft.Ref[ft.TextField](),
    "observacoes": ft.Ref[ft.TextField]()
}

feedback_sintese = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white", 
    width=500,
    height=25,
    border_radius=10
)

def atualizar_feedback_sintese(cor, msg):
    feedback_sintese.bgcolor = cor
    feedback_sintese.content.value = msg
    if feedback_sintese.page:
        feedback_sintese.update()


def mudar_cor_campo_sintese(e):
    for rotulo in rotulo_componente:
        if rotulo == e.control.label:
            componente = rotulo_componente[rotulo]
            componentes[componente].current.border_color = "black"
            componentes[componente].current.focused_border_color = "#3C618B"
            componentes[componente].current.update()


def voltar(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = ft.colors.BLACK
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    tela_principal.atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go('1')
    atualizar_feedback_sintese("white", "")


def obter_dados_finais():
    dicionario = {}
    for chave in componentes.keys():
        dicionario[chave] = componentes[chave].current.value
    return dicionario


def salvar_sintese(e):
    permissao = True
    for i, chave in enumerate(list(componentes.keys())[:3]):
        if not componentes[chave].current.value.strip():
            componentes[chave].current.border_color = ft.colors.RED
            componentes[chave].current.update()
            permissao = False
            atualizar_feedback_sintese("red", "Campo(s) obrigatório(s) não preenchido(s).")
    if permissao:
        dados_finais = obter_dados_finais()
        controle.dados_sintese[tela_principal.artigo][tela_principal.leitor] = dados_finais
        print(dados_finais)
        bd.atualizar_dados_sintese(controle.dados_sintese)
        voltar(e)
        tela_principal.atualizar_feedback(
            f'A síntese do leitor "{tela_principal.leitor}" no artigo "{tela_principal.artigo}" foi modificada com sucesso.',
            "green"
        )


def sair(e):
    dados_finais = obter_dados_finais()
    if dados_finais != dados_iniciais:
        controle.pagina.open(modal_confirmacao)
    else:
        voltar(e)


campo_artigo = ft.TextField(
    label="Artigo",
    disabled=True,
    value=" ",
    width=largura,
    border="underline"
)

campo_leitor = ft.TextField(
    label="Leitor",
    disabled=True,
    value=" ",
    width=largura,
    border="underline"
)

def atualizar_sintese():
    global dados_iniciais
    dados_iniciais = controle.dados_sintese[tela_principal.artigo][tela_principal.leitor]
    for chave in componentes:
        componentes[chave].current.value = dados_iniciais[chave]
    campo_artigo.value = tela_principal.artigo
    campo_leitor.value = tela_principal.leitor


modal_confirmacao = ft.AlertDialog(
    modal=True,
    title=ft.Text("Confirmação"),
    bgcolor="white",
    content=ft.Text("Você quer sair sem salvar as alterações?"),
    actions=[
        ft.ElevatedButton(
            "Sim",
            icon="CHECK",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=200,
            on_click=voltar
        ),
        ft.ElevatedButton(
            "Não",
            icon="CLEAR",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=200,
            on_click=lambda e: controle.pagina.close(modal_confirmacao)
        )
    ]
)

def view():
    return ft.View(
        route="Tela de Síntese",
        controls=[
            ft.Image(src=CAMINHO_SINTESE, width=1920, height=123, fit="COVER"),
            ft.Container(
                content=ft.Column(
                    controls=[
                        campo_artigo,
                        campo_leitor
                    ] +
                    [
                        ft.TextField(
                            label=rotulo,
                            ref=componentes[rotulo_componente[rotulo]],
                            on_change=mudar_cor_campo_sintese,
                            border="underline",
                            width=largura,
                            multiline=True
                        ) for rotulo in rotulo_componente
                    ] + 
                    [
                        feedback_sintese,
                        ft.Row(
                            controls=[
                                criar_botao_sair(sair, "Sair"),
                                criar_botao_salvar(salvar_sintese, "Salvar e Sair")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=30
            )
        ],
        padding=0,
        bgcolor=ft.colors.WHITE,
        scroll=ft.ScrollMode.AUTO
    )