import controle
import flet as ft
import banco_de_dados as bd
import validacoes as val

componentes = {
        'dt_tabela': ft.Ref[ft.DataTable](),
        'tf_pesquisa': ft.Ref[ft.TextField](),
        'tf_novo_leitor': ft.Ref[ft.TextField](),
    }

#------------------------------------------------------------------------ FUNCOES -------------------------------------------------------------------------------
def limpar_pesquisa(e):
    componentes["tf_pesquisa"].current.value = ""
    controle.pagina.update()

def adicionar_leitor(e:ft.ControlEvent):
    """Essa funcao vai adicionar uma nova coluna de leitor (no maximo 10) e atualizar o banco de dados com o novo leitor"""
    
    nome_leitor = componentes["tf_novo_leitor"].current.value

    #verificando se o nome de leitor ja existe
    if len(bd.obter_dados_tabela()) > 0: #arquivo nao ta vazio
        leitor_existe = nome_leitor not in bd.obter_dados_tabela()[0][6:]

    else: #ta vazio
        leitor_existe = False #retornando false pra n entrar no if

    #atualizando a tabela se nao atingiu o maximo de leitores, se o nome nao for vazio, se o arquivo nao ta vazio e se o leitor nao existe ainda
    if len(tabela_dados_artigos.columns) < 18 and nome_leitor != "" and leitor_existe:
        #adicionando a coluna nova na tabela
        tabela_dados_artigos.columns.append(ft.DataColumn(ft.Text(f"Leitor {len(tabela_dados_artigos.columns) - 7}")))
        
        #atualizando as linhas da tabela
        for id_linha, linha in enumerate(tabela_dados_artigos.rows):
            tabela_dados_artigos.rows[id_linha].cells.append(
                ft.DataCell(
                    ft.ElevatedButton(text=nome_leitor, on_click=abrir_sintese, key=id_linha)
                )
            )

        #atualizando todas as linhas no txt da tabela
        lista_salvar_dados_tabela = []
        for linha in [row.cells for row in tabela_dados_artigos.rows]: #pegando cada linha da tabela
            #lista de valores de cada celula da linha, menos dos 2 botoes do inicio. Essa lista ja ta transformando com o join, pra ficar certinho no arquivo
            #alem de ja dar o append na lista que vai mandar pra salvar, esse if, else ai e pra checar se for ft.text ou ft.elevatedbutton
            lista_salvar_dados_tabela.append(
                ",".join(
                    [
                        celula.content.value if type(celula.content) == ft.Text 
                        else celula.content.text for celula in linha[2:]
                    ]
                )
            )

        #mandando pro arquivo
        bd.atualizar_dados_tabela(lista_salvar_dados_tabela)
        
        #atualizando o txt da sintese
        dicionario_dados_sintese = bd.obter_dados_sintese() #carregando o dicionario da sintese
        for nome_artigo in dicionario_dados_sintese:
            dicionario_dados_sintese[nome_artigo][nome_leitor] = {"objetivo": "", "contribuicoes": "", "lacunas" : "", "observacoes": ""}

        #mandando pro arquivo
        bd.atualizar_dados_sintese(dicionario_dados_sintese)
        
        #atualizando a pagina
        tabela_dados_artigos.update()

        #fechando o modal e resetando a ref do nome do leitor
        controle.pagina.close(modal_nome_leitor)
        componentes["tf_novo_leitor"] = ""

        limpar_pesquisa(e)

def deletar_artigo(e:ft.ControlEvent):
    #pegando o id do artigo
    id_linha = e.control.key
    
    #tirando o artigo da lista de artigos e salvando ele numa variavel
    lista_artigos = bd.obter_dados_tabela()
    artigo_removido = lista_artigos.pop(id_linha)

    #salvando no arquivo da tabela
    lista_artigos = [",".join(linha) for linha in lista_artigos]
    
    bd.atualizar_dados_tabela(lista_artigos)

    #salvando no arquivo de sintese
    dic_artigo_sintese = bd.obter_dados_sintese()  #carregando o dicionario
    dic_artigo_sintese.pop(artigo_removido[0], None)    #removendo o artigo baseado no nome do artigo removido (indice 0)

    bd.atualizar_dados_sintese(dic_artigo_sintese)

    #atualizando a tabela da tela principal e resetando a referencia de pesquisa
    atualizar_leitores(bd.obter_dados_tabela())     #rows
    limpar_pesquisa(e)

def editar_artigo(e):
    controle.id_artigo_edicao = e.control.key

    limpar_pesquisa(e)

    controle.pagina.go("4")

def abrir_sintese(e:ft.ControlEvent):
    global leitor
    global artigo
    
    leitor = e.control.text
    artigo = bd.obter_dados_tabela()[e.control.key][0]

    #resetando a referencia de pesquisa
    limpar_pesquisa(e)

    controle.pagina.go("3")

def atualizar_leitores(lista_artigos:list):
    """Essa funcao serve pra atualizar os botoes os leitores ao mudar ou adicionar uma sintese na tela de sintese"""

    #resetando as linhas
    tabela_dados_artigos.rows = []

    for id_linha, linha in enumerate(lista_artigos): #carregando cada linha do arquivo
        #criando os valores da linha pra cada coluna, comecando pelos 2 botoes

        lista_colunas = [
            ft.DataCell(
                ft.IconButton(
                    icon=ft.Icons.DELETE, 
                    icon_color="#1E3A8A",
                    tooltip="REMOVER", 
                    key=id_linha, 
                    on_click=deletar_artigo
                )
            ),
            ft.DataCell(
                ft.IconButton(
                    icon=ft.Icons.EDIT, 
                    icon_color="#1E3A8A",
                    tooltip="EDITAR", 
                    key=id_linha, 
                    on_click=editar_artigo
                )
            )
        ]

        #adicionando cada valor da linha nessa lista, texto para os valores que nao sao leitores
        for id_coluna, coluna in enumerate(linha):
            #OUTROS VALORES
            if id_coluna <= 5:
                lista_colunas.append(ft.DataCell(ft.Text(coluna)))
            
            #LEITORES (ja adicionando o botao com a cor certa caso a sintese ja exista)
            else:
                #pegando a sintese do leitor (carregando o dicionario do txt, entrando no dicionario com o nome do artigo, dps no dicionario do leitor e, por fim, resgatando a chave objetivo)
                sintese_leitor = bd.obter_dados_sintese()[linha[0]][coluna]["objetivo"]
                
                lista_colunas.append(
                    ft.DataCell(
                        ft.ElevatedButton(
                            text=coluna, 
                            color="#212121"  if sintese_leitor == "" else "#EDEDED",
                            bgcolor="#FFFFFF" if sintese_leitor == "" else "#1E3A8A", 
                            on_click=abrir_sintese, 
                            key=id_linha
                        )
                    )
                )

        #dando o append da linha se o arquivo nao estiver vazio
        if len(lista_artigos) > 0:
            tabela_dados_artigos.rows.append(ft.DataRow(cells=lista_colunas))

def pesquisar_artigo(e):
    #Pegando a ref da esquisa
    pesquisa = componentes['tf_pesquisa'].current.value
    
    #atualizando a tabela com a lista filtrada 
    atualizar_leitores([artigo for artigo in bd.obter_dados_tabela() if val.achar_nome_tela_principal(pesquisa, artigo)])
    tabela_dados_artigos.update()
    

#---------------------------------------------------------------------- VARIAVEIS ---------------------------------------------------------------------
modal_nome_leitor = ft.AlertDialog(
    modal=True,
    title=ft.Text("Digite o nome do leitor"),
    content=ft.TextField(label="Nome", ref=componentes['tf_novo_leitor']),                    #REFERENCIADO PRA SALVAR O NOME DO NOVO LEITOR
    actions=[
        ft.ElevatedButton("Cancelar", on_click=lambda e: controle.pagina.close(modal_nome_leitor)),  #BOTAO DE VOLTAR E FECHAR O MODAL
        ft.ElevatedButton("Adicionar", on_click=adicionar_leitor),                             #BOTAO DE CRIAR O LEITOR E FECHAR O MODAL
    ],
    actions_alignment=ft.MainAxisAlignment.END
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
        ft.DataColumn(ft.Text("Local de\nPublicação")),
        ft.DataColumn(ft.Text("Abstracts"))
    ]
)

#----------------------------------------------------------------- ATUALIZANDO A DATA BASE INICIAl ------------------------------------------------------------

#adicionando as colunas dos leitores que ja estavam no banco de dados, considerando a lista apenas a partir do leitor 1, por isso o [6:]
if len(bd.obter_dados_tabela()) > 0:
    for id_coluna, coluna in enumerate(bd.obter_dados_tabela()[0][6:]):
        tabela_dados_artigos.columns.append(ft.DataColumn(ft.Text(f"Leitor {id_coluna + 1}")))

#adicionando as linhas que ja estavam no banco de dados
atualizar_leitores(bd.obter_dados_tabela())

#------------------------------------------------------------------------- VIEW -----------------------------------------------------------------------
def view():
    return ft.View(
        "Tela Principal",
        [
            ft.TextField(
                ref=componentes['tf_pesquisa'], 
                label='Pesquisar', 
                icon='search', 
                on_change=pesquisar_artigo
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Adicionar Artigo", 
                        icon=ft.Icons.ADD, 
                        on_click=lambda e: controle.pagina.go("2")
                    ),
                    ft.ElevatedButton(
                        text="Adicionar Leitor", 
                        icon=ft.Icons.ADD, 
                        on_click=lambda e: controle.pagina.open(modal_nome_leitor)
                    )
                ]
            ),
            ft.Row([tabela_dados_artigos], scroll=ft.ScrollMode.ALWAYS)
        ],
        scroll=ft.ScrollMode.ALWAYS
    )