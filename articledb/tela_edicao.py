import os

import flet as ft

from articledb import tela_principal
from articledb import controle
from articledb import banco_de_dados as bd
from articledb.tela_cadastro import obter_campo_leitores, rotulo_dica
from articledb.tela_sintese import modal_confirmacao
from articledb.tela_principal import atualizar_feedback_tela_principal
from articledb.utils import largura
from articledb.validacoes import validar_titulo, validar_link, validar_autores, validar_ano, validar_local, validar_abstracts


CAMINHO_EDICAO = os.path.join("imagens", "edicao.png")

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

feedback_edicao = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white", 
    width=largura,
    height=25,
    border_radius=10
)

def atualizar_feedback_edicao(msg, cor):
    feedback_edicao.content.value = msg
    feedback_edicao.bgcolor = cor
    if feedback_edicao.page:
        feedback_edicao.update()


def mudar_cor_campo(e):
    for rotulo in rotulo_componente:
        if rotulo == e.control.label:
            componente = rotulo_componente[rotulo]
            componentes[componente].current.border_color = "black"
            componentes[componente].current.focused_border_color = "#3C618B"
            componentes[componente].current.update()
    if all(componentes[chave].current.value.strip() for chave in list(componentes.keys())):
        atualizar_feedback_edicao("", "white")


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
        voltar_e2p(e)


def voltar_e2p(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = ft.colors.BLACK
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    tela_principal.atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go('1')
    atualizar_feedback_edicao("white", "")


def salvar_edicao(e):

    funcoes_validacao = [
        validar_titulo, validar_link, validar_autores,
        validar_ano, validar_local, validar_abstracts
    ]

    campos = []

    for i, chave in enumerate(componentes):
        if not funcoes_validacao[i](componentes[chave].current.value):
            campos.append(list(rotulo_componente.keys())[i])
            componentes[chave].current.border_color = ft.colors.RED
            componentes[chave].current.update()
    
    if campos and len(campos) == 1:
        atualizar_feedback_edicao(f'O campo "{campos[0]}" é inválido.', "red")
    
    elif campos and len(campos) > 1:
        atualizar_feedback_edicao(f'Os campos "{", ".join(campos)}" são inválidos.', "red")

    dados_finais = obter_dados_finais() + dados_iniciais[6:]
    dados_tabela = bd.obter_dados_tabela()
    dados_sintese = bd.obter_dados_sintese()
    titulo_antigo = dados_iniciais[0]
    titulo_novo = dados_finais[0]

    titulo_nao_existe = True
    for linha in dados_tabela:
        if titulo_antigo != titulo_novo and titulo_novo.upper() == linha[0].upper():
            atualizar_feedback_edicao(f'Já existe um artigo cadastrado com esse título.', "red")
            titulo_nao_existe = False
            componentes["titulo"].current.border_color = ft.colors.RED
            componentes["titulo"].current.update()

    if not campos and titulo_nao_existe:
        dados_tabela[tela_principal.id_artigo] = dados_finais

        bd.atualizar_dados_tabela(["|".join(linha) for linha in dados_tabela])

        dados_sintese = bd.obter_dados_sintese()

        if dados_sintese and titulo_novo != titulo_antigo:
            dados_sintese[titulo_novo] = dados_sintese[titulo_antigo]
            del dados_sintese[titulo_antigo]
            bd.atualizar_dados_sintese(dados_sintese)
        
        voltar_e2p(e)
        atualizar_feedback_tela_principal(f'O artigo "{titulo_antigo}" foi editado com sucesso.', "green")

    

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
                            on_change=mudar_cor_campo,
                            width=largura,
                            border="underline",
                            hint_text=rotulo_dica[rotulo],
                            hint_style=ft.TextStyle(color="#BABABA")
                        )
                        for rotulo in rotulo_componente
                    ]
                    + [
                        ft.TextField(
                            label=f"Leitor {i + 1}",
                            value=leitor,
                            disabled=True,
                            width=largura,
                            border="underline"
                        ) for i, leitor in enumerate(obter_campo_leitores()) if existe_leitor
                    ] +
                    [
                        feedback_edicao,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Sair",
                                    on_click=sair,
                                    icon="ARROW_BACK",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=295
                                ),
                                ft.ElevatedButton(
                                    "Salvar e Sair",
                                    on_click=salvar_edicao,
                                    icon="SAVE",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=295
                                )
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
