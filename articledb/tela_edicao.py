import os

import flet as ft

from articledb import tela_principal
from articledb import controle
from articledb import banco_de_dados as bd
from articledb.tela_sintese import modal_confirmacao
from articledb.tela_cadastro import (
    mudar_cor_campo_registro,
    rotulo_componente,
    componentes,
    obter_campo_leitores,
)
from articledb.tela_principal import atualizar_feedback_tela_principal
from articledb.feedback import feedback_registro, atualizar_feedback_registro
from articledb.utils import LARGURA_CAMPO, criar_botao_sair, criar_botao_salvar


CAMINHO_EDICAO = os.path.join("imagens", "edicao.png")


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


def sair_confirmacao(e):
    dados_finais = obter_dados_finais() + dados_iniciais[6:]
    if dados_iniciais != dados_finais:
        controle.pagina.open(modal_confirmacao)
    else:
        voltar_e2p(e)


def voltar_e2p(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = ft.colors.BLACK
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    tela_principal.atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go("1")
    atualizar_feedback_registro("white", "")


def salvar_edicao(e):
    permissao = True
    for i, chave in enumerate(componentes):
        if not componentes[chave].current.value.strip():
            componentes[chave].current.border_color = ft.colors.RED
            componentes[chave].current.update()
            permissao = False
            atualizar_feedback_registro(
                "red", "Campo(s) obrigatório(s) não preenchido(s)."
            )
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

        voltar_e2p(e)
        atualizar_feedback_tela_principal(
            f"O artigo '{titulo_antigo}' foi editado com sucesso.", "green"
        )


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
            on_click=voltar_e2p,
        ),
        ft.ElevatedButton(
            "Não",
            icon="CLEAR",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=200,
            on_click=lambda e: controle.pagina.close(modal_confirmacao),
        ),
    ],
)


# View
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
                            on_change=mudar_cor_campo_registro,
                            width=LARGURA_CAMPO,
                            border="underline",
                        )
                        for rotulo in rotulo_componente
                    ]
                    + [
                        ft.TextField(
                            label=f"Leitor {i + 1}",
                            value=leitor,
                            disabled=True,
                            width=500,
                            border="underline",
                        )
                        for i, leitor in enumerate(obter_campo_leitores())
                        if existe_leitor
                    ]
                    + [
                        feedback_registro,
                        ft.Row(
                            controls=[
                                criar_botao_sair(sair_confirmacao, "Sair"),
                                criar_botao_salvar(salvar_edicao, "Salvar e Sair"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=30,
            ),
        ],
        padding=0,
        bgcolor=ft.colors.WHITE,
        scroll=ft.ScrollMode.AUTO,
    )
