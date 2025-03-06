import flet as ft

def view():
    return ft.View(
                "Tela de Edicao",
                [
                    ft.Container(content=ft.Text("Edicao", size=20)),
                    ft.TextField(label='Nome')
                ]
            )