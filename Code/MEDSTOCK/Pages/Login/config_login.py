import flet as ft
import ctypes

def config_login_page(page):
    from Pages import maximize_window, minimize_window
    page.theme_mode = ft.ThemeMode.LIGHT
    
    if page.web:
        page.title = "Login"
    elif page.platform.value == "windows":
        page.window.resizable = True
        page.window.full_screen = False
        page.window_frameless = True

        page.add(
            ft.ResponsiveRow([
                ft.WindowDragArea(
                    ft.Container(
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        padding=0,
                        content=ft.Row([
                            ft.Row([
                                ft.Image(src="assets/favicon.png", width=50, height=50),
                                ft.Text("MedStock", size=30),
                            ]),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.icons.MINIMIZE_OUTLINED, on_click=lambda _: minimize_window(page), icon_color=ft.colors.BLACK),
                                    ft.IconButton(icon=ft.icons.CHECK_BOX_OUTLINE_BLANK, on_click=lambda _: maximize_window(page),icon_color=ft.colors.BLACK),
                                    ft.IconButton(icon=ft.icons.CLOSE_OUTLINED, on_click=lambda _: page.window.close(),icon_color=ft.colors.BLACK),
                                ],
                                spacing=2
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN 
                        ),
                    ),
                )
            ])
        )


def toggle_password_visibility(password_input, icon_button):
    password_input.password = not password_input.password
    icon_button.icon = ft.icons.VISIBILITY_OFF if password_input.password else ft.icons.VISIBILITY
    password_input.update()
    icon_button.update()
