import flet as ft
import controle

largura = 500

componentes = {
    "objetivo": ft.Ref[ft.TextField](),
    "contribuicoes": ft.Ref[ft.TextField](),
    "lacunas": ft.Ref[ft.TextField](),
    "observacoes": ft.Ref[ft.TextField]()
}

def mudar_cor_objetivo(e):
    componentes["objetivo"].current.border_color = ft.colors.BLACK
    componentes["objetivo"].current.focused_border_color = "#3c618b"
    componentes["objetivo"].current.update()


def mudar_cor_contribuicoes(e):
    componentes["contribuicoes"].current.border_color = ft.colors.BLACK
    componentes["contribuicoes"].current.focused_border_color = "#3c618b"
    componentes["contribuicoes"].current.update()


def mudar_cor_lacunas(e):
    componentes["lacunas"].current.border_color = ft.colors.BLACK
    componentes["lacunas"].current.focused_border_color = "#3c618b"
    componentes["lacunas"].current.update()


def mudar_cor_observacoes(e):
    componentes["observacoes"].current.border_color = ft.colors.BLACK
    componentes["observacoes"].current.focused_border_color = "#3c618b"
    componentes["observacoes"].current.update()


def abrir_modal(e):
    controle.pagina.open(modal)


def fechar_modal(e):
        controle.pagina.close(modal)


objetivo = ft.Container(
     content=ft.TextField(
          label="Objetivo",
          ref=componentes["objetivo"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_objetivo,
     )
)

contribuicoes = ft.Container(
     content=ft.TextField(
          label="Principais Contribuições",
          ref=componentes["contribuicoes"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_contribuicoes,
     )
)

lacunas = ft.Container(
     content=ft.TextField(
          label="Lacunas Encontradas",
          ref=componentes["lacunas"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_lacunas,
     )
)

observacoes = ft.Container(
     content=ft.TextField(
          label="Outras Observações",
          ref=componentes["observacoes"],
          width=largura,
          multiline=True,
          on_change=mudar_cor_observacoes,
     )
)

modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmação"),
        content=ft.Text("Você quer sair sem salvar as alterações?"),
        actions=[
            ft.TextButton("Sim", on_click=fechar_modal),
            ft.TextButton("Não", on_click=fechar_modal),
        ],
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
                    ft.ElevatedButton("Salvar e Sair", on_click=salvar),
                    ft.ElevatedButton("Abrir Modal", on_click=abrir_modal)
                ]
            )


def sair(e):
    controle.pagina.go('1')


def salvar(e):
    if not componentes["objetivo"].current.value.strip():
        componentes["objetivo"].current.border_color = ft.colors.RED
        componentes["objetivo"].current.update()
    if not componentes["contribuicoes"].current.value.strip():
        componentes["contribuicoes"].current.border_color = ft.colors.RED
        componentes["contribuicoes"].current.update()
    if not componentes["lacunas"].current.value.strip():
        componentes["lacunas"].current.border_color = ft.colors.RED
        componentes["lacunas"].current.update()
    if all(componentes[chave].current.value.strip() for chave in list(componentes.keys())[:3]):
        print('AAA')
