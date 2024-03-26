import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket


class Facerecognitionscreen:
    def __init__(self):
        self.loading_pr = None
        self.event_id = None
    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.loading_pr = ft.ProgressRing(
            visible=True,
            width=30,height=30,stroke_width=3
        )
        self.event_id = params.get('event_id')
        return  ft.View(
            f'/face_recognition/{self.event_id}',
            controls=[
                ft.Container(
                    ft.Text(
                        value=self.event_id
                    )
                )
            ]
        )