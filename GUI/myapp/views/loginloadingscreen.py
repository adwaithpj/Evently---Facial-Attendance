import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket
import time


class LoginLoadingScreen:
    def __init__(self):
        self.loading_pr = None


    def view(self, page: ft.Page, params: Params, basket: Basket):

        self.loading_pr = ft.ProgressRing(
            visible=True,
            width=30,height=30,stroke_width=3
        )

        def show_loading(e):
            print('Loading...')
            time.sleep(3)
            self.loading_pr.visible = False
            page.update()
            page.go('/login')


        return  ft.View(
            '/',
            padding=0,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=padding.all(20),
                    alignment=ft.Alignment(0,1),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            self.loading_pr,
                            ft.Text(
                                value='Loading'
                            ),
                            ft.IconButton(
                                icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                                autofocus=True,
                                on_focus=show_loading
                            )
                        ]
                    )
                )
            ]
        )
