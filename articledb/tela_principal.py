import controle
import flet as ft

componentes = {
        'tabela': ft.Ref[ft.DataTable](),
        'tf_pesquisa': ft.Ref[ft.TextField]()
        #add todos os compontens da tela aqui
    }

def view():
    return ft.View(
        "tela2",
        [
            ft.TextField(ref=componentes['tf_pesquisa'], label='pesquisar', icon='search'),
            ft.ElevatedButton(text="Criar coluna de leitor", icon=ft.Icons.ADD),
            ft.Row(
                [
                    ft.DataTable(
                        ref=componentes['tabela'],
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
                            ft.DataColumn(ft.Text("Leitor 1")),
                            ft.DataColumn(ft.Text("Leitor 2")),
                            ft.DataColumn(ft.Text("Leitor 3")),
                            ft.DataColumn(ft.Text("Leitor 4")),
                            ft.DataColumn(ft.Text("Leitor 5")),
                            ft.DataColumn(ft.Text("Leitor 6")),
                            ft.DataColumn(ft.Text("Leitor 7")),
                            ft.DataColumn(ft.Text("Leitor 8")),
                            ft.DataColumn(ft.Text("Leitor 9")),
                            ft.DataColumn(ft.Text("Leitor 10")),
                        ],
                        rows= [ft.DataRow(cells=[ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, tooltip="REMOVER")),ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, tooltip="EDITAR")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("AAAAAAAAAAAAAAAAAAAAAAAAa")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A")),ft.DataCell(ft.Text("A"))]) for i in range(0, 50)]
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
        ],
        scroll=ft.ScrollMode.ALWAYS,
    )


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
