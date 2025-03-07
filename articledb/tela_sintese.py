import flet as ft
import controle
import banco_de_dados as bd
import tela_principal
import os

CAMINHO_SINTESE = os.path.join("articledb", "imagens", "sintese.png")

dados_bd = bd.obter_dados_sintese()

largura = 500

componentes = {
    "objetivo": ft.Ref[ft.TextField](),
    "contribuicoes": ft.Ref[ft.TextField](),
    "lacunas": ft.Ref[ft.TextField](),
    "observacoes": ft.Ref[ft.TextField]()
}

def mudar_cor_campo(e):
    campo = e.control.label
    if campo == "Objetivo":
        componentes["objetivo"].current.border_color = ft.colors.BLACK
        componentes["objetivo"].current.focused_border_color = "#3C618B"
        componentes["objetivo"].current.update()
    if campo == "Principais Contribuições":
        componentes["contribuicoes"].current.border_color = ft.colors.BLACK
        componentes["contribuicoes"].current.focused_border_color = "#3C618B"
        componentes["contribuicoes"].current.update()
    if campo == "Lacunas Encontradas":
        componentes["lacunas"].current.border_color = ft.colors.BLACK
        componentes["lacunas"].current.focused_border_color = "#3C618B"
        componentes["lacunas"].current.update()
    if campo == "Outras Observações":
        componentes["observacoes"].current.border_color = ft.colors.BLACK
        componentes["observacoes"].current.focused_border_color = "#3C618B"
        componentes["observacoes"].current.update()


def voltar(e):
    for chave in componentes.keys():
        componentes[chave].current.border_color = ft.colors.BLACK
        componentes[chave].current.focused_border_color = "#3C618B"
        componentes[chave].current.update()
    tela_principal.atualizar_tabela(bd.obter_dados_tabela())
    controle.pagina.go('1')


def abrir_modal(e):
    controle.pagina.open(modal)


def fechar_modal(e):
    controle.pagina.close(modal)


def obter_dados_finais():
    dicionario = {}
    for chave in componentes.keys():
        dicionario[chave] = componentes[chave].current.value
    return dicionario


def salvar_e_sair(e):
    permissao = True
    for chave in list(componentes.keys())[:3]:
        if not componentes[chave].current.value.strip():
            componentes[chave].current.border_color = ft.colors.RED
            componentes[chave].current.update()
            permissao = False
    if permissao:
        dados_finais = obter_dados_finais()
        dados_bd[tela_principal.artigo][tela_principal.leitor] = dados_finais
        bd.atualizar_dados_sintese(dados_bd)
        voltar(e)
        tela_principal.atualizar_mensagem_feedback(
            f'A síntese do leitor "{tela_principal.leitor}" no artigo "{tela_principal.artigo}" foi modificada com sucesso.', ft.colors.GREEN
        )


def atualizar_sintese(e):
    global dados_iniciais
    dados_iniciais = dados_bd[tela_principal.artigo][tela_principal.leitor]
    for chave in componentes.keys():
        componentes[chave].current.value = dados_iniciais[chave]


def sair(e):
    dados_finais = obter_dados_finais()
    if dados_finais != dados_iniciais:
        abrir_modal(e)
    else:
        voltar(e)


artigo = ft.TextField(
    label="Artigo",
    disabled=True,
    value=" ",
    width=largura,
    border="underline"
)

leitor = ft.TextField(
    label="Leitor",
    disabled=True,
    value=" ",
    width=largura,
    border="underline"
)

objetivo = ft.Container(
    content=ft.TextField(
        label="Objetivo",
        ref=componentes["objetivo"],
        width=largura,
        multiline=True,
        on_change=mudar_cor_campo,
        border="underline"
    )
)

contribuicoes = ft.Container(
     content=ft.TextField(
        label="Principais Contribuições",
        ref=componentes["contribuicoes"],
        width=largura,
        multiline=True,
        on_change=mudar_cor_campo,
        border="underline"
    )
)

lacunas = ft.Container(
     content=ft.TextField(
        label="Lacunas Encontradas",
        ref=componentes["lacunas"],
        width=largura,
        multiline=True,
        on_change=mudar_cor_campo,
        border="underline"
    )
)

observacoes = ft.Container(
     content=ft.TextField(
        label="Outras Observações",
        ref=componentes["observacoes"],
        width=largura,
        multiline=True,
        on_change=mudar_cor_campo,
        border="underline"
    )
)

modal = ft.AlertDialog(
    modal=True,
    title=ft.Text("Confirmação"),
    content=ft.Text("Você quer sair sem salvar as alterações?"),
    actions=[
        ft.TextButton("Sim", on_click=voltar),
        ft.TextButton("Não", on_click=fechar_modal)
    ]
)

def atualizar_sintese(e):
    global dados_iniciais
    dados_iniciais = dados_bd[tela_principal.artigo][tela_principal.leitor]
    for chave in componentes.keys():
        componentes[chave].current.value = dados_iniciais[chave]
    artigo.value = tela_principal.artigo
    leitor.value = tela_principal.leitor


def view():
    return ft.View(
        "Tela de Síntese",
        controls=[
            ft.Image(src=CAMINHO_SINTESE, width=1920, height=123, fit="COVER"),
            ft.Container(
                content=ft.Column(
                    [
                        artigo,
                        leitor,
                        objetivo,
                        contribuicoes,
                        lacunas,
                        observacoes,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Sair",
                                    on_click=sair,
                                    icon="ARROW_BACK",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=245
                                ),
                                ft.ElevatedButton(
                                    "Salvar e Sair", 
                                    on_click=salvar_e_sair, 
                                    icon="SAVE",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon_color="white",
                                    width=245
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=30
            )
        ],
        padding=0,
        bgcolor=ft.colors.WHITE,
    )