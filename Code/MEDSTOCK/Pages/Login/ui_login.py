import flet as ft
from flet import *
from .back_login import login_button_clicked, reset_password_button_clicked
from .config_login import config_login_page, toggle_password_visibility

def login_page(page: ft.Page):
    
    config_login_page(page)
    
    # Campo de email
    email_input = ft.TextField(
        label="Email", 
        width=500,
        height=50,
        text_align="start"
    )
    
    password_input = ft.TextField(
        label="Password",
        password=True,
        width=500,
        height=50,
        text_align="start",
        suffix=ft.IconButton(
            icon_size=20,
            width=30,
            height=30,
            icon=ft.icons.VISIBILITY_OFF,
            on_click=lambda e: toggle_password_visibility(password_input, e.control),
            padding=ft.padding.all(2)
        )
    )
    
    # Botão de login
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda _: login_button_clicked(email_input, password_input), 
        height=60,
        width=200,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=25)
        )
    )
    
    reset_password_text = ft.TextButton(
        on_click=lambda _: reset_password_button_clicked, 
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(value="Esqueci-me da Palavra-Passe", size=15),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
                ),
                padding=ft.padding.all(10),
    ),
        )
    

    img_login = ft.Image(
        src=f"Logo/Superior/PNG/Logo.png",
        fit=ft.ImageFit.FILL,
        width=1200,
        height=500,
    )
    
    login_container = ft.Container(
        content=ft.Column(
            [
                img_login,
                email_input,
                password_input,
                login_button,
                reset_password_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=False
        ),
        alignment=ft.alignment.center,
    )

    page.add(login_container)
