import flet as ft
import controle

def main(pagina: ft.Page):   
    controle.init(pagina)
    pagina.title = "articleDB"
    pagina.on_route_change = controle.controle_de_rota
    pagina.theme_mode  = "light"
    pagina.window.min_width = 750
    pagina.window.min_height = 500
    pagina.go('1')


ft.app(target=main)