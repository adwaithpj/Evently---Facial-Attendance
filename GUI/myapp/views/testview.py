import flet as ft
from flet_core import padding
from flet_route import Params, Basket
import threading
from time import sleep

global event_id

class Testingview:

    def __init__(self):
        self.pb = ft.ProgressBar(width=400)



    def view(self, page: ft.Page, params: Params, basket: Basket):


        return ft.View(
            '/test',
            padding=padding.all(20),
            spacing=20,
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Text("Downloading"), self.pb]),
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    # on_click=on_click_run_progressbar
                ),
            ]
        )
