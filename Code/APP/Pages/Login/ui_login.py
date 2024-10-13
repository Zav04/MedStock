import flet as ft
from .back_login import login_button_clicked, reset_password_button_clicked, register_button_clicked
from .config_login import config_login_page

def login_page(page: ft.Page):
    
    config_login_page(page)
    
    
    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Senha", password=True, width=300)
    login_button = ft.ElevatedButton(text="Login", on_click=login_button_clicked(email_input, password_input))
    reset_password_text = ft.TextButton(text="Esqueci-me da Palavra-Passe", on_click=reset_password_button_clicked)
    registar_text = ft.TextButton(text="Registar", on_click=register_button_clicked)

    login_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Página de Login", size=30, weight=ft.FontWeight.BOLD),
                #ft.Image(src="assets/Logo/Lateral/ICO/Logo.ico"),
                email_input,
                password_input,
                login_button,
                registar_text,
                reset_password_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.Padding(left=20, right=20, top=20, bottom=20),
    )

    page.add(
        ft.Row(
            [
                login_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True 
        )
    )
