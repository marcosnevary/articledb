import controle
import flet as ft
import banco_de_dados as bd

componentes = {
        'dt_tabela': ft.Ref[ft.DataTable](),
        'tf_pesquisa': ft.Ref[ft.TextField](),
        'tf_novo_leitor': ft.Ref[ft.TextField](),
    }

#------------------------------------------------------------------------ FUNCOES -------------------------------------------------------------------------------
def adiciona_leitor(e:ft.ControlEvent):
    """Essa funcao vai adicionar uma nova coluna de leitor (no maximo 10) e atualizar o banco de dados com o novo leitor"""
    
    nome_leitor = componentes["tf_novo_leitor"].current.value

    #verificando se o nome de leitor ja existe
    if len(bd.carregando_dados_tabela()) > 0: #arquivo nao ta vazio
        leitor_existe = nome_leitor not in bd.carregando_dados_tabela()[0][6:]

    else: #ta vazio
        leitor_existe = False #retornando false pra n entrar no if

    #atualizando a tabela se nao atingiu o maximo de leitores, se o nome nao for vazio, se o arquivo nao ta vazio e se o leitor nao existe ainda
    if len(tabela_dados_artigos.columns) < 18 and nome_leitor != "" and leitor_existe:
        #adicionando a coluna nova na tabela
        tabela_dados_artigos.columns.append(ft.DataColumn(ft.Text(f"Leitor {len(tabela_dados_artigos.columns) - 7}")))
        
        #atualizando as linhas da tabela
        for id_linha, linha in enumerate(tabela_dados_artigos.rows):
            tabela_dados_artigos.rows[id_linha].cells.append(ft.DataCell(ft.ElevatedButton(text=nome_leitor, on_click=sintese_leitor, key=id_linha)))

        #atualizando todas as linhas no txt da tabela
        lista_salvar_dados_tabela = []
        for linha in [row.cells for row in tabela_dados_artigos.rows]: #pegando cada linha da tabela
            #lista de valores de cada celula da linha, menos dos 2 botoes do inicio. Essa lista ja ta transformando com o join, pra ficar certinho no arquivo
            #alem de ja dar o append na lista que vai mandar pra salvar, esse if, else ai e pra checar se for ft.text ou ft.elevatedbutton
            lista_salvar_dados_tabela.append(",".join([celula.content.value if type(celula.content) == ft.Text else celula.content.text for celula in linha[2:]]))

        #mandando pro arquivo
        bd.atualizando_dados_tabela(lista_salvar_dados_tabela)
        
        #atualizando o txt da sintese
        dicionario_dados_sintese = bd.carregando_dados_sintese() #carregando o dicionario da sintese
        for nome_artigo in dicionario_dados_sintese:
            dicionario_dados_sintese[nome_artigo][nome_leitor] = {"objetivo": "", "contribuicoes": "", "lacunas" : "", "observacoes": ""}

        #mandando pro arquivo
        bd.atualizando_dados_sinteses(dicionario_dados_sintese)
        
        #atualizando a pagina
        tabela_dados_artigos.update()

        #fechando o modal e resetando a ref do nome do leitor
        controle.pagina.close(modal_nome_leitor)
        componentes["tf_novo_leitor"] = ""

def deletar_artigo(e:ft.ControlEvent):
    #pegando o id do artigo
    id_linha = e.control.key
    
    #tirando o artigo da lista de artigos e salvando ele numa variavel
    lista_artigos = bd.carregando_dados_tabela()
    artigo_removido = lista_artigos.pop(id_linha)

    #salvando no arquivo da tabela
    lista_artigos = [",".join(linha) for linha in lista_artigos]
    
    bd.atualizando_dados_tabela(lista_artigos)

    #salvando no arquivo de sintese
    dic_artigo_sintese = bd.carregando_dados_sintese()  #carregando o dicionario
    dic_artigo_sintese.pop(artigo_removido[0], None)    #removendo o artigo baseado no nome do artigo removido (indice 0)

    bd.atualizando_dados_sinteses(dic_artigo_sintese)

    #atualizando a tabela da tela principal
    atualizar_leitores_tela_principal() #rows
    tabela_dados_artigos.update()       #tabela na tela

def editar_artigo(e):
    controle.id_artigo_edicao = e.control.key
    controle.pagina.go("4")

def sintese_leitor(e:ft.ControlEvent):
    botao_nome_leitor = e.control.text
    botao_id_linha = e.control.key
    
    #abrindo a sintese do leitor
    controle.nome_leitor_sintese = botao_nome_leitor
    controle.artigo_sintese = bd.carregando_dados_tabela()[botao_id_linha][0]

    controle.pagina.go("3")

def atualizar_leitores_tela_principal():
    """Essa funcao serve pra atualizar os botoes os leitores ao mudar ou adicionar uma sintese na tela de sintese"""

    #resetando as linhas
    tabela_dados_artigos.rows = []

    for id_linha, linha in enumerate(bd.carregando_dados_tabela()): #carregando cada linha do arquivo
        #criando os valores da linha pra cada coluna, comecando pelos 2 botoes
        lista_colunas = [ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, tooltip="REMOVER", key=id_linha, on_click=deletar_artigo)), ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, tooltip="EDITAR", key=id_linha, on_click=editar_artigo))]

        #adicionando cada valor da linha nessa lista, texto para os valores que nao sao leitores
        for id_coluna, coluna in enumerate(linha):
            #OUTROS VALORES
            if id_coluna <= 5: lista_colunas.append(ft.DataCell(ft.Text(coluna)))
            
            #LEITORES (ja adicionando o botao com a cor certa caso a sintese ja exista)
            else:
                #pegando a sintese do leitor (carregando o dicionario do txt, entrando no dicionario com o nome do artigo, dps no dicionario do leitor e, por fim, resgatando a chave objetivo)
                sintese_leitor = bd.carregando_dados_sintese()[linha[0]][coluna]["objetivo"]
                lista_colunas.append(ft.DataCell(ft.ElevatedButton(text=coluna, bgcolor="#FFFFFF" if sintese_leitor == "" else "#0000ff", on_click=sintese_leitor, key=id_linha)))

        #dando o append da linha se o arquivo nao estiver vazio
        if len(bd.carregando_dados_tabela()) > 0: tabela_dados_artigos.rows.append(ft.DataRow(cells=lista_colunas))

# def filtrar_dados(query):
#     return [
#             ft.DataRow(cells=preencher_linha_tabela(cadastro))
#             for cadastro in con.banco_de_dados
#             if query in cadastro['nome'] or query in cadastro['telefone']
#         ]

# def pesquisar(e):
#     query = componentes['tf_pesquisa'].current.value
#     componentes['tabela'].current.rows = filtrar_dados(query)
#     con.page.update()

# def atualizar(e):
#     usuario = e.control.key    
#     con.tela_atualizar.init(usuario)
#     con.page.go('3')


#---------------------------------------------------------------------- VARIAVEIS ---------------------------------------------------------------------
modal_nome_leitor = ft.AlertDialog(
        modal=True,
        title=ft.Text("Digite o nome do leitor"),
        content=ft.TextField(label="Digite aqui", ref=componentes['tf_novo_leitor']),                    #REFERENCIADO PRA SALVAR O NOME DO NOVO LEITOR
        actions=[
            ft.ElevatedButton("Cancelar", on_click=lambda e: controle.pagina.close(modal_nome_leitor)),  #BOTAO DE VOLTAR E FECHAR O MODAL
            ft.ElevatedButton("Adicionar Leitor", on_click=adiciona_leitor),                             #BOTAO DE CRIAR O LEITOR E FECHAR O MODAL
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

tabela_dados_artigos = ft.DataTable(
                        ref=componentes['dt_tabela'],
                        show_bottom_border=True,
                        columns=[
                            ft.DataColumn(ft.Text("Remover")),
                            ft.DataColumn(ft.Text("Editar")),
                            ft.DataColumn(ft.Text("Título")),
                            ft.DataColumn(ft.Text("Link")),
                            ft.DataColumn(ft.Text("Autores")),
                            ft.DataColumn(ft.Text("Ano")),
                            ft.DataColumn(ft.Text(" Local de\nPublicação")),
                            ft.DataColumn(ft.Text("Abstracts")),
                        ])

#----------------------------------------------------------------- ATUALIZANDO A DATA BASE INICIAl ------------------------------------------------------------

#adicionando as colunas dos leitores que ja estavam no banco de dados, considerando a lista apenas a partir do leitor 1, por isso o [6:]
if len(bd.carregando_dados_tabela()) > 0:
    for id_coluna, coluna in enumerate(bd.carregando_dados_tabela()[0][6:]):
        tabela_dados_artigos.columns.append(ft.DataColumn(ft.Text(f"Leitor {id_coluna + 1}")))

#adicionando as linhas que ja estavam no banco de dados
atualizar_leitores_tela_principal()

#------------------------------------------------------------------------- VIEW -----------------------------------------------------------------------
def view():
    return ft.View(
        "tela principal",
        [
            #TEXTFIELD DA PESQUISA
            ft.TextField(ref=componentes['tf_pesquisa'], label='pesquisar', icon='search'),
            
            #LINHA DE ADICIONAR NOVO LEITOR E CADASTRAR NOVO ARTIGO
            ft.Row([
                ft.ElevatedButton(text="Adicionar Artigo", icon=ft.Icons.ADD, on_click=lambda e: controle.pagina.go("2")),                  #INDO PRA TELA DE CADASTRO
                ft.ElevatedButton(text="Adicionar Leitor", icon=ft.Icons.ADD, on_click=lambda e: controle.pagina.open(modal_nome_leitor)),  #ABRINDO O MODAL
            ]),

            #LINHA COM A TABELA DE DADOS DOS ARTIGOS
            ft.Row([tabela_dados_artigos], scroll=ft.ScrollMode.ALWAYS),
        ],
        scroll=ft.ScrollMode.ALWAYS, #SCROLL DA TELA
    )