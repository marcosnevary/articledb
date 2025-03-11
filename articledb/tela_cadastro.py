import flet as ft
import banco_de_dados as bd
import controle

# Os campos que estão fixados
componentes = {
    "titulo": ft.Ref[ft.TextField](),
    "link": ft.Ref[ft.TextField](),
    "autores": ft.Ref[ft.TextField](),
    "ano": ft.Ref[ft.TextField](),
    "local": ft.Ref[ft.TextField](),
    "abstracts": ft.Ref[ft.TextField]()
}

def validar_campos():
    """Vê se tá tudo preenchido pra continuar"""
    for campo in componentes.values():
        if not campo.current.value.strip():
            campo.current.border_color = ft.colors.RED
            campo.current.update()
            return False
    return True

def salvar_cadastro(e):
    """Guarda o artigo e prepara espaço pros leitores preencherem depois!"""

    if not validar_campos():
        return  # Impede o salvamento setiver campos vazios

    # Cria uma lista com os dados do artigo
    artigo = [campo.current.value for campo in componentes.values()]

    # Carrega os dados já cadastrados
    dados_tabela = bd.obter_dados_tabela()
    dados_sintese = bd.obter_dados_sintese()

    #Se o artigo ainda não tá cadastrado, reserva um espaço pra ele
    titulo = artigo[0]  #A gente usa o titulo do artigo como chave
    if titulo not in dados_sintese:
        dados_sintese[titulo] = {}

    # Identifica leitores na tabela
    leitores = dados_tabela[0][6:] if dados_tabela and len(dados_tabela[0]) > 6 else []

    # Cria um dicionário para cada leitor
    for leitor in leitores:
        dados_sintese[titulo][leitor]= {
            "objetivo": "",
            "contribuicoes": "",
            "lacunas": "",
            "observacoes": ""
        }


    # Atualiza os arquivos
    dados_tabela.append(artigo)  # Adiciona o novo artigo
    bd.atualizar_dados_tabela([",".join(linha) for linha in dados_tabela])
    bd.atualizar_dados_sintese(dados_sintese)

    # Voltar para a tela principal
    controle.pagina.go("1")

def view():
    """Cria a tela de cadastro do artigo."""
    return ft.View(
        "Cadastro de Artigo",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cadastro de Artigo", size=24, weight=ft.FontWeight.BOLD)
                    ] + [
                        ft.TextField(label=label.capitalize(), ref=ref, width=400)
                        for label, ref in componentes.items()
                    ] + [
                        ft.Row(
                            [
                                ft.ElevatedButton(text="Salvar", on_click=salvar_cadastro),
                                ft.ElevatedButton(text="Cancelar", on_click=lambda e: controle.pagina.go("1"))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        )
                    ],
                    spacing=10
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        ],
        bgcolor=ft.colors.WHITE,
        scroll=ft.ScrollMode.AUTO
    )