import flet as ft
import banco_de_dados as bd
import controle
from tela_principal import atualizar_tabela
import os
from utils import largura
from time import sleep

CAMINHO_CADASTRO = os.path.join("articledb", "imagens", "cadastro.png")

rotulo_componente = {
    "Título": "titulo",
    "Link": "link",
    "Autores": "autores",
    "Ano": "ano",
    "Local de Publicação": "local",
    "Abstracts": "abstracts"
}

componentes = {
    "titulo": ft.Ref[ft.TextField](),
    "link": ft.Ref[ft.TextField](),
    "autores": ft.Ref[ft.TextField](),
    "ano": ft.Ref[ft.TextField](),
    "local": ft.Ref[ft.TextField](),
    "abstracts": ft.Ref[ft.TextField]()
}

feedback = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white", 
    width=500,
    height=25,
    border_radius=10
)

def mudar_feedback(cor, msg):
    feedback.bgcolor = cor
    feedback.content.value = msg
    if feedback.page:
        feedback.update()
    

def mudar_cor_campo(e):
    for rotulo in rotulo_componente:
        if rotulo == e.control.label:
            componente = rotulo_componente[rotulo]
            componentes[componente].current.border_color = "black"
            componentes[componente].current.focused_border_color = "#3C618B"
            componentes[componente].current.update()


def voltar(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = "black"
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go('1')
    mudar_feedback("white", "")
    for chave in componentes:
        componentes[chave].current.value = ""


def salvar_cadastro(e):
    """Guarda o artigo e prepara espaço pros leitores preencherem depois!"""
    
    permissao = True

    for i, chave in enumerate(componentes.keys()):
        if not componentes[chave].current.value.strip():
            componentes[chave].current.border_color = ft.colors.RED
            componentes[chave].current.update()
            permissao = False
            mudar_feedback("red", "Campo(s) obrigatório(s) não preenchido(s).")
            if i == len(componentes) - 1:
                sleep(10)
                mudar_feedback("white", "")

    if permissao:
        artigo = [campo.current.value for campo in componentes.values()]

        dados_tabela = bd.obter_dados_tabela()
        dados_sintese = bd.obter_dados_sintese()

        titulo = artigo[0]
        if titulo not in dados_sintese:
            dados_sintese[titulo] = {}

        leitores = dados_tabela[0][6:] if dados_tabela and len(dados_tabela[0]) > 6 else []

        for leitor in leitores:
            dados_sintese[titulo][leitor]= {
                "objetivo": "",
                "contribuicoes": "",
                "lacunas": "",
                "observacoes": ""
            }
        
        dados_tabela.append(artigo + leitores)
        bd.atualizar_dados_tabela(["|".join(linha) for linha in dados_tabela])
        bd.atualizar_dados_sintese(dados_sintese)

        voltar(e)


def view():
    return ft.View(
        route="Tela de Cadastro",
        controls=[
            ft.Image(src=CAMINHO_CADASTRO, width=1920, height=123, fit="COVER"),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.TextField(
                            label=rotulo,
                            ref=componentes[rotulo_componente[rotulo]],
                            width=largura,
                            on_change=mudar_cor_campo,
                            border="underline"
                        ) for rotulo in rotulo_componente
                    ] +
                    [
                        feedback,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Sair",
                                    on_click=voltar,
                                    icon="CLEAR",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=245
                                ),
                                ft.ElevatedButton(
                                    "Adicionar",
                                    on_click=salvar_cadastro,
                                    icon="ADD",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=245
                                )
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