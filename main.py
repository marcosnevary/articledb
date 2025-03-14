import flet as ft
import articledb.controle

def main(pagina: ft.Page):   
    articledb.controle.init(pagina)
    pagina.title = "articleDB"
    pagina.on_route_change = articledb.controle.controle_de_rota
    pagina.theme_mode  = "light"
    pagina.window.min_width = 750
    pagina.window.min_height = 700
    pagina.go('1')


ft.app(target=main)