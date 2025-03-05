import tela_principal, tela_cadastro, tela_sintese, tela_edicao
import flet as ft
import banco_de_dados as bd

def init(p):
    global pagina, telas, banco_de_dados, id_artigo_edicao
    pagina = p
    id_artigo_edicao = None
    
    telas = {
        "1": tela_principal.view(),
        #"2": tela_cadastro.view(),
        "3": tela_sintese.view(),
        #"4": tela_edicao.view(),
    }


def controle_de_rota(route_event):
    pagina.views.clear()    
    if pagina.route == "3":
        tela_sintese.atualizar_sintese('')
    pagina.views.append(telas[route_event.route])        
    pagina.update()