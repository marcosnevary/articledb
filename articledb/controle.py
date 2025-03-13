import tela_principal, tela_cadastro, tela_sintese, tela_edicao
import flet as ft
import banco_de_dados as bd

def init(p):
    global pagina, telas, banco_de_dados
    dados_tabela = bd.obter_dados_tabela()
    pagina = p
    id_artigo_edicao = None

    telas = {
        "1": tela_principal.view(),
        "2": tela_cadastro.view(True),
        "3": tela_sintese.view(),
        "4": tela_edicao.view(True),
    }


def controle_de_rota(route_event):
    pagina.views.clear()
    if pagina.route == "2":
        dados_tabela = bd.obter_dados_tabela()
        if dados_tabela:
            telas["2"] = tela_cadastro.view(True)
        else:
            telas["2"] = tela_cadastro.view(False)
            
    if pagina.route == "3":
        global dados_sintese
        dados_sintese = bd.obter_dados_sintese()
        tela_sintese.atualizar_sintese()

    if pagina.route == "4":
        global dados_edicao
        dados_edicao = bd.obter_dados_tabela()
        if dados_edicao:
            telas["4"] = tela_edicao.view(True)
        else:
            telas["4"] = tela_edicao.view(False)
        tela_edicao.atualizar_edicao()

    pagina.views.append(telas[route_event.route])  
    pagina.update()