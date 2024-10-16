import flet as ft
import threading
import functools

alert_containers = []

def show_overlay(page: ft.Page, message: str, alert_type: str):
    if alert_type == "error":
        bgcolor = ft.colors.RED_100
        border_color = ft.colors.RED_600
        icon = ft.icons.ERROR_OUTLINE
    elif alert_type == "success":
        bgcolor = ft.colors.GREEN_100
        border_color = ft.colors.GREEN_600
        icon = ft.icons.CHECK_CIRCLE_OUTLINE
    elif alert_type =="warning":
        bgcolor = ft.colors.YELLOW_100
        border_color = ft.colors.YELLOW_900
        icon = ft.icons.WARNING_OUTLINED
    
    alert_container = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icon, color=border_color, size=30),
                    padding=ft.Padding(0, 0, 15, 0),
                ),
                ft.Text(
                    message, 
                    color=border_color,
                    max_lines=None,
                    expand=True,
                    overflow=ft.TextOverflow.VISIBLE
                ),
                ft.IconButton(
                    icon=ft.icons.CLOSE, 
                    on_click=lambda e: close_alert(page, alert_container),
                    icon_color=border_color
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        ),
        padding=10,
        bgcolor=bgcolor,
        border_radius=8,
        border=ft.border.all(2, border_color),
        width=300,
        alignment=ft.alignment.center
    )

    alert_containers.append(alert_container)
    page.overlay.append(alert_container)
    update_alert_positions(page)
    page.update()

    timer = threading.Timer(5, functools.partial(close_alert, page, alert_container))
    timer.start()


def update_alert_positions(page: ft.Page):
    for idx, alert_container in enumerate(alert_containers):
        if page.platform == "windows":
            alert_container.top = 80 + (idx * 80)
            alert_container.right = 10
        else:
            alert_container.top = 10 + (idx * 80)
            alert_container.right = 10

def close_alert(page: ft.Page, alert_container: ft.Container):
    if alert_container in alert_containers:
        alert_containers.remove(alert_container)
        page.overlay.remove(alert_container)
        update_alert_positions(page)
        page.update()
