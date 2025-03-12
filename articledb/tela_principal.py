import controle
import flet as ft
import banco_de_dados as bd
import validacoes as val
import os
from time import sleep

CAMINHO_INICIO = os.path.join("articledb", "imagens", "inicio.png")

componentes = {
    'tf_pesquisa': ft.Ref[ft.TextField](),
    'tf_novo_leitor': ft.Ref[ft.TextField](),
    'id_linha_excluir_artigo': "",
}

tabela = ft.DataTable(
    show_bottom_border=True,
    columns=[
        ft.DataColumn(ft.Text("Excluir", weight="bold")),
        ft.DataColumn(ft.Text("Editar", weight="bold")),
        ft.DataColumn(ft.Text("Título", weight="bold")),
        ft.DataColumn(ft.Text("Link", weight="bold")),
        ft.DataColumn(ft.Text("Autores", weight="bold")),
        ft.DataColumn(ft.Text("Ano", weight="bold")),
        ft.DataColumn(ft.Text("Local de\nPublicação", weight="bold")),
        ft.DataColumn(ft.Text("Abstracts", weight="bold"))
    ]
)


def atualizar_tabela(lista_artigos):
    """
    Essa funcao serve pra atualizar as linhas da tabela ao excluir/adicionar/pesquisar artigos
    ou ao adicionar uma sintese na tela de sintese
    """

    tabela.rows = [] #limpando as linhas da tabela

    for id_linha, linha in enumerate(lista_artigos): #pegando cada linha do artigo recebido na funcao
        lista_colunas = [ #criando os 2 botoes (remover e editar) da linha final
            ft.DataCell(
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.DELETE, 
                        icon_color="#1E3A8A", 
                        tooltip="Excluir", 
                        key=id_linha, 
                        on_click=abrir_modal_excluir
                    )
                )
            ),
            ft.DataCell(
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.EDIT, 
                        icon_color="#1E3A8A",
                        tooltip="Editar", 
                        key=id_linha, 
                        on_click=editar_artigo
                    )
                )
            )
        ]

        for id_coluna, coluna in enumerate(linha): #pegando cada item da linha da lista recebida e adicionando na linha final
            if id_coluna <= 5: #informacoes do artigo
                lista_colunas.append(ft.DataCell(ft.Text(coluna)))
            
            else: #leitores
                sintese_leitor = bd.obter_dados_sintese()[linha[0]][coluna]["objetivo"] #pegando a sintese do leitor, no caso apenas o objetivo (vai mudar a cor do botao)
                
                lista_colunas.append(
                    ft.DataCell(
                        ft.Container(
                            ft.ElevatedButton(
                                text=coluna, 
                                color="#212121" if sintese_leitor == "" else "#FFFFFF",
                                bgcolor="#FFFFFF" if sintese_leitor == "" else "#3254B4",
                                on_click=abrir_sintese, 
                                key=id_linha,
                            ),
                            alignment=ft.alignment.center_right
                        )
                    )
                )

        if len(lista_artigos) > 0: #adicionando a linha final na tabela se a lista recebida nao estiver vazia
            tabela.rows.append(ft.DataRow(cells=lista_colunas))


def pesquisar_artigo(e):
    """Basicamente vai pesquisar os artigos"""
    pesquisa = componentes['tf_pesquisa'].current.value #pegando o texto da pesquisa

    atualizar_tabela( #atualizando a tabela com a lista de artigos que deram match com a pesquisa
        [
            artigo for artigo in bd.obter_dados_tabela() 
            if val.achar_nome_tela_principal(pesquisa, artigo) #verifica se deu match
        ]
    )

    tabela.update()


def limpar_pesquisa(e):
    """Basicamente limpa a barra pesquisa"""
    componentes["tf_pesquisa"].current.value = ""
    controle.pagina.update()


def adicionar_leitor(e:ft.ControlEvent):
    """
    Essa funcao vai adicionar uma nova coluna de leitor (no maximo 10) e 
    atualizar o banco de dados com o novo leitor
    """
    
    nome_leitor = componentes["tf_novo_leitor"].current.value

    dados_tabela = bd.obter_dados_tabela()

    if dados_tabela: #verifica se o leitor ja existe caso exista algum dado
        leitor_existe = nome_leitor in dados_tabela[0][6:]
    else:
        return
    
    if not nome_leitor.strip(): #nome digitado é vazio
        componentes["tf_novo_leitor"].current.border_color = ft.colors.RED
        componentes["tf_novo_leitor"].current.update()
        
    elif len(tabela.columns) < 18 and not leitor_existe: #nome nao e vazio, tem espaco pra mais leitores e o leitor ainda nao existe
        tabela.columns.append( #adicionando a coluna nova na tabela
            ft.DataColumn(
                ft.Row(
                    [
                        ft.PopupMenuButton(
                            icon= ft.Icons.MORE_VERT,
                            items=
                            [
                                ft.PopupMenuItem(
                                    content=ft.Row(
                                        [
                                            ft.Icon(
                                                name=ft.Icons.DELETE, 
                                                color="#1E3A8A", 
                                                key=len(tabela.columns) - 8,
                                            ),
                                            ft.Text("Remover")
                                        ]
                                    ),
                                    on_click=remover_leitor,
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row(
                                        [
                                            ft.Icon(
                                                name=ft.Icons.EDIT, 
                                                color="#1E3A8A",
                                                key=len(tabela.columns) - 8,
                                            ),
                                            ft.Text("Editar")
                                        ]
                                    ),
                                    on_click=editar_leitor,
                                )
                            ]
                        ),
                        ft.Text(f"Leitor {len(tabela.columns) - 7}", weight="bold"),
                    ]
                )
            )
        )
        
        for indice, linha in enumerate(tabela.rows): #adicionando o botao de leitor em cada linha
            tabela.rows[indice].cells.append(
                ft.DataCell(
                    ft.Container(
                        ft.ElevatedButton(
                            text=nome_leitor,
                            bgcolor="white",
                            color="#212121",
                            on_click=abrir_sintese, 
                            key=indice
                        ),
                        alignment=ft.alignment.center_right
                    )
                )
            )

        dados_tabela_atualizado = [] #criando a lista atualizada que vai ser enviada pro arquivo
        for linha in [row.cells for row in tabela.rows]:
            dados_tabela_atualizado.append(
                "|".join(
                    [
                        celula.content.value if type(celula.content) == ft.Text  #textos
                        else celula.content.content.text for celula in linha[2:] #nome do leitor dentro do texto do botao, dentro do container, dentro do datacell
                    ]
                )
            )

        bd.atualizar_dados_tabela(dados_tabela_atualizado) #enviando pro arquivo
        
        dados_sintese = bd.obter_dados_sintese() #criando o dicionario atualizado que vai ser enviado pro arquivo
        for nome_artigo in dados_sintese:
            dados_sintese[nome_artigo][nome_leitor] = {
                "objetivo": "",
                "contribuicoes": "",
                "lacunas" : "",
                "observacoes": ""
            }

        bd.atualizar_dados_sintese(dados_sintese) #enviando pro arquivo
        
        tabela.update() #atualizando a tabela
        fechar_modal_leitor(e)
        limpar_pesquisa(e)


def mudar_cor_campo(e):
    """Vai alterar a cor do campo de leitor"""
    componentes["tf_novo_leitor"].current.border_color = "black"
    componentes["tf_novo_leitor"].current.focused_border_color = "#3C618B"
    componentes["tf_novo_leitor"].current.update()


def fechar_modal_leitor(e):
    controle.pagina.close(modal_leitor)
    componentes["tf_novo_leitor"].current.value = ""  #resetando o valor do componente


modal_leitor = ft.AlertDialog(
    modal=True,
    title=ft.Text("Digite o nome do leitor"),
    content=ft.TextField(
        label="Nome",
        ref=componentes['tf_novo_leitor'],
        on_change=mudar_cor_campo,
        input_filter=ft.InputFilter(regex_string=r"^[a-zA-ZÃÁÀÂãàáâÊÁÈêéèÍÎÌîíìÓÔÒÕóôòõÚÛÙúûùç\s]*$"),
        border="underline"
    ),
    actions=[
        ft.ElevatedButton(
            "Cancelar",
            on_click=fechar_modal_leitor,
            icon="CLEAR",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=120
        ),
        ft.ElevatedButton(
            "Adicionar",
            on_click=adicionar_leitor,
            icon="ADD",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=120
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    bgcolor=ft.colors.WHITE
)


def atualizar_feedback(msg, cor):
    txt_mensagem_feedback.value = msg
    container_mensagem_feedback.bgcolor = cor

    controle.pagina.update()

    #voltando a cor e texto ao original
    sleep(10)
    txt_mensagem_feedback.value = ""
    container_mensagem_feedback.bgcolor = "white"

    controle.pagina.update()


txt_mensagem_feedback = ft.Text(value = "", expand=True, color=ft.colors.WHITE)


container_mensagem_feedback = ft.Container(
    content=txt_mensagem_feedback,
    bgcolor=ft.colors.WHITE,
    width=2000,
    expand=True,
    alignment=ft.alignment.center,
    height=25,
    border_radius=10
)


def excluir_artigo(e):
    """Basicamente vai pegar a linha do artigo e abrir o modal de excluir"""
    id_linha = int(componentes["id_linha_excluir_artigo"]) #pegando o id do artigo salvo nos componentes
    
    dados_tabela = bd.obter_dados_tabela()         #lista de todos os artigos
    artigo_excluido = dados_tabela.pop(id_linha)   #removendo o artigo baseado no indice da linha e salvando ele em uma variavel

    dados_tabela = ["|".join(linha) for linha in dados_tabela] #criando a lista atualizada q vai ser enviada pro arquivo

    bd.atualizar_dados_tabela(dados_tabela) #enviando pro arquivo

    dados_sintese = bd.obter_dados_sintese()       #carregando o dicionario do arquivo
    dados_sintese.pop(artigo_excluido[0], None)    #removendo o dicionario do artigo, usando o nome (indice 0) salvo na variavel

    bd.atualizar_dados_sintese(dados_sintese) #enviando pro arquivo

    atualizar_tabela(bd.obter_dados_tabela())
    limpar_pesquisa(e)
    fechar_modal_excluir(e)

    if not dados_tabela: #removendo as colunas de leitores se nao tem mais artigos e se tiver algum leitor
        if len(tabela.columns) > 8:
            tabela.columns = tabela.columns[:8]
            tabela.update()

    atualizar_feedback(f"O artigo '{artigo_excluido[0]}' foi excluído com sucesso.", ft.colors.RED)
    

def abrir_modal_excluir(e):
    componentes["id_linha_excluir_artigo"] = str(e.control.key) #salvando o id do artigo nos componentes
    controle.pagina.open(modal_excluir)


def fechar_modal_excluir(e):
    componentes["id_linha_excluir_artigo"] = "" #resetando o valor do componente
    controle.pagina.close(modal_excluir)


modal_excluir = ft.AlertDialog(
    modal=True,
    title=ft.Text("Você deseja excluir esse artigo?"),
    actions=[
        ft.ElevatedButton(
            "Sim",
            on_click=excluir_artigo,
            icon="CHECK",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=200
        ),
        ft.ElevatedButton(
            "Não",
            on_click=fechar_modal_excluir,
            icon="CLEAR",
            color="white",
            bgcolor="#3254B4",
            icon_color="white",
            width=200
        )
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    bgcolor=ft.colors.WHITE
)


def editar_artigo(e):
    """Vai abrir a tela de edicao de artigo, repassando pra ela o id do artigo"""
    global id_artigo

    id_artigo = e.control.key

    limpar_pesquisa(e)

    controle.pagina.go("4")


def abrir_sintese(e):
    global leitor
    global artigo
    
    leitor = e.control.text
    artigo = bd.obter_dados_tabela()[e.control.key][0]

    limpar_pesquisa(e)

    controle.pagina.go("3")


def remover_leitor(e):

    print(e.control.content.controls[0].key)

    pass


def editar_leitor(e):
    print(e.control.content.controls[0].key)

    pass


#criando as colunas iniciais dos leitores caso exista algum artigo no arquivo e caso exista algum leitor no arquivo
dados_tabela = bd.obter_dados_tabela()
if dados_tabela:
    if len(dados_tabela[0]) > 6:
        for id_coluna, coluna in enumerate(dados_tabela[0][6:]):   #lista apenas dos nomes dos leitores
            tabela.columns.append(                                 #criando as colunas de leitores com os botoes de excluir e editar
                ft.DataColumn(
                    ft.Row(
                        [
                            ft.PopupMenuButton(
                                icon= ft.Icons.MORE_VERT,
        	                    items=
                                [
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(
                                                    name=ft.Icons.DELETE, 
                                                    color="#1E3A8A", 
                                                    key=id_coluna,
                                                ),
                                                ft.Text("Remover")
                                            ]
                                        ),
                                        on_click=remover_leitor,
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(
                                                    name=ft.Icons.EDIT, 
                                                    color="#1E3A8A",
                                                    key=id_coluna,
                                                ),
                                                ft.Text("Editar")
                                            ]
                                        ),
                                        on_click=editar_leitor,
                                    )
                                ]
                            ),
                            ft.Text(f"Leitor {id_coluna + 1}", weight="bold"),
                        ]
                    )
                )
            )

#atualizando a tabela inicialmente
atualizar_tabela(dados_tabela)

def view():
    return ft.View(
        route="Tela Principal",
        controls=[
            ft.Image(src=CAMINHO_INICIO, width=1920, height=123, fit="COVER"),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.TextField(
                                    ref=componentes["tf_pesquisa"],
                                    label="Pesquisar",
                                    icon='search', 
                                    on_change=pesquisar_artigo,
                                    expand=True,
                                    border="underline"
                                ),
                                ft.ElevatedButton(
                                    text="Adicionar Artigo",
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon=ft.Icons.ADD,
                                    icon_color="white",
                                    on_click=lambda e: controle.pagina.go("2"),
                                ),
                                ft.ElevatedButton(
                                    text="Adicionar Leitor", 
                                    color="white",
                                    bgcolor="#3254B4",
                                    icon=ft.Icons.ADD,
                                    icon_color="white",
                                    on_click=lambda e: controle.pagina.open(modal_leitor),
                                )
                            ]
                        ),
                        container_mensagem_feedback,
                        ft.Container(
                            content=ft.Row([tabela], scroll=ft.ScrollMode.ALWAYS),
                            border=ft.border.all(1.2, "black"),  # Adiciona borda fixa
                            border_radius=10,
                            padding=0.4,
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.Padding(left=100, top=30, bottom=30, right=100)
            )
        ],
        scroll=ft.ScrollMode.HIDDEN,
        bgcolor=ft.colors.WHITE,
        padding=0,
    )