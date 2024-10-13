import flet as ft


def config_login_page(page):
    from Pages import maximize_window, minimize_window
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    if page.web:
        page.title = "Login"
        page.icon = "assets/icon.png"
    elif page.platform.value == "windows":
        page.window.resizable = True
        page.window.full_screen = False
        page.window.icon = "assets/Icons/Logo.ico"
        page.window.frameless = True
        page.appbar = ft.AppBar(
            title=ft.Text("MedStock"),
            leading=ft.Image(src="assets/Logo/Lateral/ICO/Logo.ico"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(icon=ft.icons.MINIMIZE,on_click=lambda _:minimize_window(page)),
                ft.IconButton(icon=ft.icons.MAXIMIZE,on_click=lambda _:maximize_window(page)),
                ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda _:page.window.close()),
            ],
        )