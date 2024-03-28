import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket
class Testingview:

    def view(self, page: ft.Page, params: Params, basket: Basket):
        return ft.View(
            '/test',
            padding=padding.all(20),
            spacing=20,
            controls=[
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=lambda e: page.go('/face_recognition/1')
                ),

            ]
        )