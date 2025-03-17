import os
import datetime

import flet as ft

from articledb import banco_de_dados as bd
from articledb import controle
from articledb.tela_principal import atualizar_tabela, atualizar_feedback_tela_principal
from articledb.validacoes import validar_titulo, validar_link, validar_autores, validar_ano, validar_local, validar_abstracts
from articledb import validacoes
from articledb.utils import largura


CAMINHO_CADASTRO = os.path.join("imagens", "cadastro.png")


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


rotulo_dica = {
    "Título": "",
    "Link": "Deve começar com http:// ou https:// (exemplo: https://x.com)",
    "Autores": "Autor1, Autor2, Autor3 etc.",
    "Ano": f"Entre 1665 e {datetime.datetime.now().year}",
    "Local de Publicação": "Cidade",
    "Abstracts": ""
}


feedback_cadastro = ft.Container(
    content=ft.Text(value="", color="white"),
    alignment=ft.alignment.center,
    bgcolor="white", 
    width=largura,
    height=25,
    border_radius=10
)

def atualizar_feedback_cadastro(msg, cor):
    feedback_cadastro.content.value = msg
    feedback_cadastro.bgcolor = cor
    if feedback_cadastro.page:
        feedback_cadastro.update()


def mudar_cor_campo(e):
    for rotulo in rotulo_componente:
        if rotulo == e.control.label:
            componente = rotulo_componente[rotulo]
            componentes[componente].current.border_color = "black"
            componentes[componente].current.focused_border_color = "#3C618B"
            componentes[componente].current.update()
    if all(componentes[chave].current.value.strip() for chave in list(componentes.keys())):
        atualizar_feedback_cadastro("", "white")


def voltar_c2p(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = "black"
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go('1')
    atualizar_feedback_cadastro("", "white")
    for chave in componentes:
        componentes[chave].current.value = ""


def salvar_cadastro(e):
    """Guarda o artigo e prepara espaço pros leitores preencherem depois!"""

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
        atualizar_feedback_cadastro(f'O campo "{campos[0]}" é inválido.', "red")
    
    elif campos and len(campos) > 1:
        atualizar_feedback_cadastro(f'Os campos "{", ".join(campos)}" são inválidos.', "red")

    dados_tabela = bd.obter_dados_tabela()
    dados_sintese = bd.obter_dados_sintese()
    artigo = [campo.current.value for campo in componentes.values()]
    titulo = artigo[0]

    titulo_nao_existe = True
    for linha in dados_tabela:
        if titulo.upper() == linha[0].upper():
            atualizar_feedback_cadastro(f'Já existe um artigo cadastrado com esse título.', "red")
            titulo_nao_existe = False
            componentes["titulo"].current.border_color = ft.colors.RED
            componentes["titulo"].current.update()

    if not campos and titulo_nao_existe:

        if titulo not in dados_sintese:
            dados_sintese[titulo] = {}

        dados_tabela = bd.obter_dados_tabela()
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

        voltar_c2p(e)
        atualizar_feedback_tela_principal(f'O artigo "{titulo}" foi adicionado com sucesso.', 'green')
        

def obter_campo_leitores():
    dados_tabela = bd.obter_dados_tabela()
    if dados_tabela:
        return dados_tabela[0][6:]
    else:
        return []


#View
def view(existe_leitor=False):
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
                            border="underline",
                            input_filter=validacoes.componente_filtro[rotulo],
                            hint_text=rotulo_dica[rotulo],
                            hint_style=ft.TextStyle(color="#BABABA"),
                        ) for rotulo in rotulo_componente
                    ] + 
                    [
                        ft.TextField(
                            label=f"Leitor {i + 1}",
                            value=leitor,
                            disabled=True,
                            width=largura,
                            border="underline"
                        ) for i, leitor in enumerate(obter_campo_leitores()) if existe_leitor
                    ] + 
                    [
                        feedback_cadastro,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Sair",
                                    on_click=voltar_c2p,
                                    icon="CLEAR",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=295
                                ),
                                ft.ElevatedButton(
                                    "Adicionar",
                                    on_click=salvar_cadastro,
                                    icon="ADD",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=295
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