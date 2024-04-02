import flet as ft
from flet_core import border_radius, margin , padding
from flet_route import Params, Basket


class AmazonS3:
    def __init__(self):
        self.pb = ft.ProgressBar(width=400)

    def view(self, page: ft.Page, params: Params, basket: Basket):
        return ft.View(
            route=f'/dwld_image/{self.event_id}',
        )
