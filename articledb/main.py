import flet as ft
import controle

def main(pagina: ft.Page):   
    controle.init(pagina)         
    pagina.title = "ArticleDB"  
    pagina.on_route_change = controle.controle_de_rota  
    pagina.theme_mode  = "light"
    pagina.go('1')
    
ft.app(target=main)
