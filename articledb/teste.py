import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text("Centralizado"),
                            width=200,
                            height=100,
                            bgcolor="blue",
                            alignment=ft.alignment.center,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,  # Expande para ocupar toda a tela
        )
    )

ft.app(target=main)
