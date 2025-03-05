import flet as ft

def main(page: ft.Page):
    container = ft.Container(
        expand=True,
        gradient=ft.RadialGradient(
            center=ft.Alignment(0, -1.25),
            radius=1.4,
            colors=[
                "#42445f"
            ]
        )
    )

    page.add(container)
    page.update()

ft.app(target=main)