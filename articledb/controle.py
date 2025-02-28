import tela_cadastro
import flet as ft
import banco_de_dados as bd
import controle

def init(p):
    global pagina, telas, banco_de_dados
    pagina = p
    telas = {
        '1': tela_cadastro.view(),
    }


def controle_de_rota(route_event):
    pagina.views.clear()    
    pagina.views.append(telas[route_event.route])          
    pagina.update()