import controle
import flet as ft
import banco_de_dados as bd

componentes = {
        'dt_tabela': ft.Ref[ft.DataTable](),
        'tf_pesquisa': ft.Ref[ft.TextField](),
        'tf_novo_leitor': ft.Ref[ft.TextField](),
    }

#---------------------------------------------------------------------- VARIAVEIS ---------------------------------------------------------------------
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

#adicionando as colunas dos leitores que ja estavam no banco de dados, considerando a lista apenas a partir do leitor 1, por isso o [6:]
if len(bd.carregando_dados_tabela()) > 0:
    for id_coluna, coluna in enumerate(bd.carregando_dados_tabela()[0].split(",")[6:]):
        tabela_dados_artigos.columns.append(ft.DataColumn(ft.Text(f"Leitor {id_coluna + 1}")))

#adicionando as linhas que ja estavam no banco de dados
for linha in bd.carregando_dados_tabela(): #carregando cada linha
    #criando os valores da linha pra cada coluna, comecando pelos 2 botoes
    lista_colunas = [ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, tooltip="REMOVER")), ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, tooltip="EDITAR"))]

    #adicionando cada valor da linha nessa lista, texto para os valores que nao sao leitores
    for id_coluna, coluna in enumerate(linha.split(",")):
        #OUTROS VALORES
        if id_coluna <= 5: lista_colunas.append(ft.DataCell(ft.Text(coluna)))
        
        #LEITORES (ja adicionando o botao com a cor certa caso a sintese ja exista)
        else:
            #pegando a sintese do leitor (carregando o dicionario do txt, entrando no dicionario com o nome do artigo, dps no dicionario do leitor e, por fim, resgatando a chave objetivo)
            sintese_leitor = bd.carregando_dados_sintese()[linha.split(",")[0]][coluna]["objetivo"]
            lista_colunas.append(ft.DataCell(ft.ElevatedButton(text=coluna, bgcolor="#FFFFFF" if sintese_leitor == "" else "#0000ff")))

    #dando o append da linha se o arquivo nao estiver vazio
    if len(bd.carregando_dados_tabela()) > 0: tabela_dados_artigos.rows.append(ft.DataRow(cells=lista_colunas))



    


#------------------------------------------------------------------------- VIEW -----------------------------------------------------------------------
def view():
    return ft.View(
        "tela principal",
        [
            #TEXTFIELD DA PESQUISA
            ft.TextField(ref=componentes['tf_pesquisa'], label='pesquisar', icon='search'),
            
            #LINHA DE ADICIONAR NOVO LEITOR
            ft.Row([
                ft.TextField(label="Nome do leitor", ref=componentes['tf_novo_leitor']), #REFERENCIADO PRA SALVAR O NOME DO NOVO LEITOR
                ft.ElevatedButton(text="Criar coluna de leitor", icon=ft.Icons.ADD, on_click=adiciona_leitor),
            ]),
            
            #BOTAO PRA CADASTRAR NOVO ARTIGO, VAI PRA TELA CADASTRO
            ft.ElevatedButton(text="Cadastrar novo artigo", icon=ft.Icons.ADD),

            #LINHA COM A TABELA DE DADOS DOS ARTIGOS
            ft.Row([tabela_dados_artigos],scroll=ft.ScrollMode.ALWAYS),
        ],
        scroll=ft.ScrollMode.ALWAYS, #SCROLL DA TELA
    )

#------------------------------------------------------------------------ FUNCOES -------------------------------------------------------------------------------
def adiciona_leitor(e):
    """Essa funcao vai adicionar uma nova coluna de leitor (no maximo 10) e atualizar o banco de dados com o novo leitor"""
    
    nome_leitor = componentes["tf_novo_leitor"].current.value

    #verificando se o nome de leitor ja existe
    if len(bd.carregando_dados_tabela()) > 0: #arquivo nao ta vazio
        leitor_existe = nome_leitor not in bd.carregando_dados_tabela()[0].split(",")[6:]

    else: #ta vazio
        leitor_existe = False #retornando false pra n entrar no if

    #atualizando a tabela se nao atingiu o maximo de leitores, se o nome nao for vazio, se o arquivo nao ta vazio e se o leitor nao existe ainda
    if len(tabela_dados_artigos.columns) < 18 and nome_leitor != "" and leitor_existe:
        #adicionando a coluna nova na tabela
        tabela_dados_artigos.columns.append(ft.DataColumn(ft.Text(f"Leitor {len(tabela_dados_artigos.columns) - 7}")))
        
        #atualizando as linhas da tabela
        for id_linha, linha in enumerate(tabela_dados_artigos.rows):
            tabela_dados_artigos.rows[id_linha].cells.append(ft.DataCell(ft.ElevatedButton(text=nome_leitor)))

        #atualizando todas as linhas no txt da tabela
        lista_salvar_dados_tabela = []
        for linha in [row.cells for row in tabela_dados_artigos.rows]: #pegando cada linha da tabela
            #lista de valores de cada celula da linha, menos dos 2 botoes do inicio. Essa lista ja ta transformando com o join, pra ficar certinho no arquivo
            #alem de ja dar o append na lista que vai mandar pra salvar, esse if, else ai e pra checar se for ft.text ou ft.elevatedbutton
            lista_salvar_dados_tabela.append(",".join([celula.content.value if type(celula.content) == ft.Text else celula.content.text for celula in linha[2:]]))

        bd.atualizando_dados_tabela(lista_salvar_dados_tabela)
        
        #atualizando o txt da sintese
        dicionario_dados_sintese = bd.carregando_dados_sintese() #carregando o dicionario da sintese
        for nome_artigo in dicionario_dados_sintese:
            dicionario_dados_sintese[nome_artigo][nome_leitor] = {"objetivo": "", "contribuicoes": "", "lacunas" : "", "observacoes": ""}

        bd.atualizando_dados_sinteses(dicionario_dados_sintese)

        tabela_dados_artigos.update()



# def atualizar_tabela():
#     return [
#             ft.DataRow(cells=preencher_linha_tabela(cadastro)) for cadastro in con.banco_de_dados
#         ]


# def preencher_linha_tabela(cadastro):
#     return [
#                 ft.DataCell(ft.Text(cadastro['nome'])),
#                 ft.DataCell(ft.Text(cadastro['telefone'])),
#                 ft.DataCell(ft.Row(
#                      [
#                             ft.IconButton(
#                                 icon=ft.icons.EDIT,
#                                 icon_color="blue",
#                                 icon_size=35,
#                                 tooltip="Atualizar",  
#                                 key=cadastro,
#                                 on_click=atualizar                              
#                             ),
#                             ft.IconButton(
#                                 icon=ft.icons.REMOVE_CIRCLE,
#                                 icon_color="red",
#                                 icon_size=35,
#                                 tooltip="Remover",
#                                 key=cadastro,
#                                 on_click=deletar
#                             ),
#                         ]
#                 ))                                                           
#         ]


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

# """
# A função deletar foi modificada para utilizar a função salvar do arquivo controle
# """
# def deletar(e):
#     usuario = e.control.key
#     con.remover(usuario)
#     componentes['tabela'].current.rows = atualizar_tabela()
#     con.page.update()

# def atualizar(e):
#     usuario = e.control.key    
#     con.tela_atualizar.init(usuario)
#     con.page.go('3')
