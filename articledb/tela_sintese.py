import flet as ft
import controle
import banco_de_dados as bd
import tela_principal

dados_bd = bd.carregando_dados_sintese()

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
    controle.artigo_sintese = ""
    controle.nome_leitor_sintese = ""

    tela_principal.atualizar_leitores_tela_principal(bd.carregando_dados_tabela())
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
        dados_bd[controle.artigo_sintese][controle.nome_leitor_sintese] = dados_finais
        bd.atualizando_dados_sinteses(dados_bd)
        voltar(e)


def sair(e):
    dados_iniciais = dados_bd[controle.artigo_sintese][controle.nome_leitor_sintese]
    for chave in componentes.keys():
        componentes[chave].current.value = dados_iniciais[chave]

    dados_finais = obter_dados_finais()
    if dados_finais != dados_iniciais:
        abrir_modal(e)
    else:
        voltar(e)


objetivo = ft.Container(
     content=ft.TextField(
          label="Objetivo",
          ref=componentes["objetivo"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_campo
     )
)

contribuicoes = ft.Container(
     content=ft.TextField(
          label="Principais Contribuições",
          ref=componentes["contribuicoes"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_campo
     )
)

lacunas = ft.Container(
     content=ft.TextField(
          label="Lacunas Encontradas",
          ref=componentes["lacunas"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_campo
     )
)

observacoes = ft.Container(
     content=ft.TextField(
          label="Outras Observações",
          ref=componentes["observacoes"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_campo
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

def view():
    return ft.View(
                "Tela de Síntese",
                [
                    objetivo,
                    contribuicoes,
                    lacunas,
                    observacoes,
                    ft.ElevatedButton("Sair", on_click=sair),
                    ft.ElevatedButton("Salvar e Sair", on_click=salvar_e_sair)
                ]
            )