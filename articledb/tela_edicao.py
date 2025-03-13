import flet as ft
import tela_principal
import controle
import banco_de_dados as bd
from tela_sintese import modal_confirmacao
from tela_cadastro import mudar_cor_campo
from tela_principal import atualizar_feedback
from utils import largura, criar_botao_sair, criar_botao_salvar
import os

CAMINHO_EDICAO = os.path.join("articledb", "imagens", "edicao.png")

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


def atualizar_edicao():
    global dados_iniciais
    dados_iniciais = controle.dados_edicao[tela_principal.id_artigo]
    for i, chave in enumerate(componentes):
        componentes[chave].current.value = dados_iniciais[i]


def obter_dados_finais():
    lista = []
    for chave in componentes:
        lista.append(componentes[chave].current.value)
    return lista


def sair(e):
    dados_finais = obter_dados_finais() + dados_iniciais[6:]
    if dados_iniciais != dados_finais:
        controle.pagina.open(modal_confirmacao)
    else:
        voltar(e)


def voltar(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = ft.colors.BLACK
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    tela_principal.atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go('1')
    mudar_feedback("white", "")


def salvar_edicao(e):
    permissao = True
    for i, chave in enumerate(componentes):
        if not componentes[chave].current.value.strip():
            componentes[chave].current.border_color = ft.colors.RED
            componentes[chave].current.update()
            permissao = False
            mudar_feedback("red", "Campo(s) obrigatório(s) não preenchido(s).")
    if permissao:
        dados_finais = obter_dados_finais() + dados_iniciais[6:]
        dados_tabela = bd.obter_dados_tabela()

        dados_tabela[tela_principal.id_artigo] = dados_finais

        bd.atualizar_dados_tabela(["|".join(linha) for linha in dados_tabela])

        titulo_antigo = dados_iniciais[0]
        titulo_novo = dados_finais[0]
        dados_sintese = bd.obter_dados_sintese()

        if dados_sintese and titulo_novo != titulo_antigo:
            dados_sintese[titulo_novo] = dados_sintese[titulo_antigo]
            del dados_sintese[titulo_antigo]
            bd.atualizar_dados_sintese(dados_sintese)
        
        atualizar_feedback(f"O artigo '{titulo_antigo}' foi editado com sucesso.", ft.colors.RED)
        voltar(e)
    

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

def obter_campo_leitores():
    dados_tabela = bd.obter_dados_tabela()
    if dados_tabela:
        return dados_tabela[0][6:]
    else:
        return []


def view(existe_leitor: bool):
    return ft.View(
        route="Tela de Edição",
        controls=[
            ft.Image(src=CAMINHO_EDICAO, width=1920, height=123, fit="COVER"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.TextField(
                            label=rotulo,
                            ref=componentes[rotulo_componente[rotulo]],
                            on_change=mudar_cor_campo,
                            width=largura,
                            border="underline"
                        ) for rotulo in rotulo_componente
                    ] + [
                        ft.TextField(
                            label=f"Leitor {i + 1}",
                            value=leitor,
                            disabled=True,
                            width=500,
                            border="underline"
                        ) for i, leitor in enumerate(obter_campo_leitores()) if existe_leitor
                    ] +
                    [
                        feedback,
                        ft.Row(
                            controls=[
                                criar_botao_sair(sair, "Sair"),
                                criar_botao_salvar(salvar_edicao, "Salvar e Sair")
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