import flet as ft
from flet import *
from Pages import login_page


def main(page: ft.Page):
    login_page(page)

#web
ft.app(target=main, assets_dir="assets", host="localhost", port=9000, view="web_browser", web_renderer="html")
#app
#ft.app(target=main, assets_dir="assets", view="flet_app")
