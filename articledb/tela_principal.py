import controle
import flet as ft
import banco_de_dados as bd
import validacoes as val

componentes = {
        'dt_tabela': ft.Ref[ft.DataTable](),
        'tf_pesquisa': ft.Ref[ft.TextField](),
        'tf_novo_leitor': ft.Ref[ft.TextField](),
    }

tabela = ft.DataTable(
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

def limpar_pesquisa(e):
    componentes["tf_pesquisa"].current.value = ""
    controle.pagina.update()


def adicionar_leitor(e:ft.ControlEvent):
    """
    Essa funcao vai adicionar uma nova coluna de leitor (no maximo 10) e 
    atualizar o banco de dados com o novo leitor
    """
    
    nome_leitor = componentes["tf_novo_leitor"].current.value

    dados_tabela = bd.obter_dados_tabela()

    if dados_tabela:
        leitor_existe = nome_leitor in dados_tabela[0][6:]

    if not nome_leitor.strip():
        componentes["tf_novo_leitor"].current.border_color = ft.colors.RED
        componentes["tf_novo_leitor"].current.update()
    elif len(tabela.columns) < 18 and not leitor_existe:
        tabela.columns.append(
            ft.DataColumn(ft.Text(f"Leitor {len(tabela.columns) - 7}"))
        )
        
        for indice, linha in enumerate(tabela.rows):
            tabela.rows[indice].cells.append(
                ft.DataCell(
                    ft.ElevatedButton(
                        text=nome_leitor, 
                        on_click=abrir_sintese, 
                        key=indice
                    )
                )
            )

        dados_tabela_atualizado = []
        for linha in [row.cells for row in tabela.rows]:
            dados_tabela_atualizado.append(
                ",".join(
                    [
                        celula.content.value if type(celula.content) == ft.Text 
                        else celula.content.text for celula in linha[2:]
                    ]
                )
            )

        bd.atualizar_dados_tabela(dados_tabela_atualizado)
        
        dados_sintese = bd.obter_dados_sintese()
        for nome_artigo in dados_sintese:
            dados_sintese[nome_artigo][nome_leitor] = {
                "objetivo": "",
                "contribuicoes": "",
                "lacunas" : "",
                "observacoes": ""
            }

        bd.atualizar_dados_sintese(dados_sintese)
        
        tabela.update()

        fechar_modal_leitor(e)
        limpar_pesquisa(e)


def deletar_artigo(e:ft.ControlEvent):
    id_linha = e.control.key
    
    lista_artigos = bd.obter_dados_tabela()
    artigo_removido = lista_artigos.pop(id_linha)

    print(artigo_removido)

    lista_artigos = [",".join(linha) for linha in lista_artigos]
    
    bd.atualizar_dados_tabela(lista_artigos)

    dic_artigo_sintese = bd.obter_dados_sintese()
    dic_artigo_sintese.pop(artigo_removido[0], None)

    bd.atualizar_dados_sintese(dic_artigo_sintese)

    atualizar_tabela(bd.obter_dados_tabela())
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

    limpar_pesquisa(e)

    controle.pagina.go("3")


def atualizar_tabela(lista_artigos:list):
    """
    Essa funcao serve pra atualizar os botoes os leitores ao mudar ou adicionar 
    uma sintese na tela de sintese
    """

    tabela.rows = []

    for id_linha, linha in enumerate(lista_artigos):
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

        for id_coluna, coluna in enumerate(linha):
            if id_coluna <= 5:
                lista_colunas.append(ft.DataCell(ft.Text(coluna)))
            
            else:
                sintese_leitor = bd.obter_dados_sintese()[linha[0]][coluna]["objetivo"]
                
                lista_colunas.append(
                    ft.DataCell(
                        ft.ElevatedButton(
                            text=coluna, 
                            color="#212121" if sintese_leitor == "" else "#EDEDED",
                            bgcolor="#FFFFFF" if sintese_leitor == "" else "#1E3A8A",
                            on_click=abrir_sintese, 
                            key=id_linha
                        )
                    )
                )

        if len(lista_artigos) > 0:
            tabela.rows.append(ft.DataRow(cells=lista_colunas))


def pesquisar_artigo(e):
    pesquisa = componentes['tf_pesquisa'].current.value

    atualizar_tabela(
        [
            artigo for artigo in bd.obter_dados_tabela() 
            if val.achar_nome_tela_principal(pesquisa, artigo)
        ]
    )
    tabela.update()


def mudar_cor_campo(e):
    componentes["tf_novo_leitor"].current.border_color = ft.colors.BLACK
    componentes["tf_novo_leitor"].current.focused_border_color = "#3C618B"
    componentes["tf_novo_leitor"].current.update()


def fechar_modal_leitor(e):
    controle.pagina.close(modal_nome_leitor)
    componentes["tf_novo_leitor"].current.value = ""


modal_nome_leitor = ft.AlertDialog(
    modal=True,
    title=ft.Text("Digite o nome do leitor"),
    content=ft.TextField(
        label="Nome",
        ref=componentes['tf_novo_leitor'],
        on_change=mudar_cor_campo
    ),
    actions=[
        ft.ElevatedButton("Cancelar", on_click=fechar_modal_leitor),
        ft.ElevatedButton("Adicionar", on_click=adicionar_leitor),
    ],
    actions_alignment=ft.MainAxisAlignment.END
)

if len(bd.obter_dados_tabela()) > 0:
    for id_coluna, coluna in enumerate(bd.obter_dados_tabela()[0][6:]):
        tabela.columns.append(ft.DataColumn(ft.Text(f"Leitor {id_coluna + 1}")))

atualizar_tabela(bd.obter_dados_tabela())

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
            ft.Row([tabela], scroll=ft.ScrollMode.ALWAYS)
        ],
        scroll=ft.ScrollMode.ALWAYS
    )