import flet as ft

def view():
    return ft.View(
                "Tela do Cadastro",
                [
                    ft.Container(content=ft.Text("Cadastro", size=20)),
                    ft.TextField(label='Nome')
                ]
            )
