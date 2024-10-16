import flet as ft
from .back_admin import handle_register
from datetime import datetime

def admin_page(page: ft.Page):
    from Pages import config_system
    
    config_system(page)

    nome_input = ft.TextField(
        label="Nome",
        width=500,
        height=50,
        text_align="start"
    )

    email_input = ft.TextField(
        label="Email",
        width=500,
        height=50,
        text_align="start"
    )
    
    sexo_input = ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Feminino")
        ],
        width=500,
        height=50,
    )
    
    dias = [ft.dropdown.Option(str(d)) for d in range(1, 32)]
    anos = [ft.dropdown.Option(str(a)) for a in range(1900, datetime.now().year + 1)]
    meses = [
        ft.dropdown.Option("01", "Janeiro"),
        ft.dropdown.Option("02", "Fevereiro"),
        ft.dropdown.Option("03", "Março"),
        ft.dropdown.Option("04", "Abril"),
        ft.dropdown.Option("05", "Maio"),
        ft.dropdown.Option("06", "Junho"),
        ft.dropdown.Option("07", "Julho"),
        ft.dropdown.Option("08", "Agosto"),
        ft.dropdown.Option("09", "Setembro"),
        ft.dropdown.Option("10", "Outubro"),
        ft.dropdown.Option("11", "Novembro"),
        ft.dropdown.Option("12", "Dezembro"),
    ]
    
    dia_input = ft.Dropdown(
        label="Dia",
        options=dias,
        width=120,
        height=50
    )
    
    mes_input = ft.Dropdown(
        label="Mês",
        options=meses,
        width=150,
        height=50
    )
    
    ano_input = ft.Dropdown(
        label="Ano",
        options=anos,
        width=230,
        height=50
    )

    data_nascimento_container = ft.Row(
        [
            dia_input,
            mes_input,
            ano_input
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=30,
        width=500
    )

    role_input = ft.Dropdown(
        label="Cargo",
        options=[
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Farmacêutico"),
            ft.dropdown.Option("Gestor Responsável"),
            ft.dropdown.Option("Enfermeiro"),
            ft.dropdown.Option("Médico"),
            ft.dropdown.Option("Secretário Clínico"),
            ft.dropdown.Option("Assistente"),     
        ],
        width=500,
        height=50,
    )

    register_button = ft.ElevatedButton(
        text="Registrar",
        on_click=lambda _: handle_register(page, nome_input, email_input, sexo_input, dia_input, mes_input, ano_input, role_input),
        height=60,
        width=200,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=25)
        )
    )
    
    register_container = ft.Container(
        content=ft.Column(
            [
                nome_input,
                email_input,
                sexo_input,
                data_nascimento_container,
                role_input,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=ft.Padding(0, 0, 0, 10)
    )

    page.add(register_container)
