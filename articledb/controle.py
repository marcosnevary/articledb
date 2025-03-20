from articledb import tela_principal, tela_cadastro, tela_sintese, tela_edicao
from articledb import banco_de_dados as bd


def init(p):
    global pagina, telas, banco_de_dados
    pagina = p

    telas = {
        "1": tela_principal.view(),
        "2": tela_cadastro.view(),
        "3": tela_sintese.view(),
        "4": tela_edicao.view(),
    }


def controle_de_rota(route_event):
    pagina.views.clear()
    if pagina.route == "2":
        dados_tabela = bd.obter_dados_tabela()
        if dados_tabela:
            telas["2"] = tela_cadastro.view()
        else:
            telas["2"] = tela_cadastro.view()

    if pagina.route == "3":
        global dados_sintese
        dados_sintese = bd.obter_dados_sintese()
        tela_sintese.atualizar_sintese()

    if pagina.route == "4":
        global dados_edicao
        dados_edicao = bd.obter_dados_tabela()
        if dados_edicao:
            telas["4"] = tela_edicao.view()
        else:
            telas["4"] = tela_edicao.view()
        tela_edicao.atualizar_edicao()

    pagina.views.append(telas[route_event.route])
    pagina.update()
