import flet as ft
from flet_route import Params, Basket


def NewNoteView(page: ft.Page, params: Params, basket: Basket):


    ref_title = ft.Ref[ft.TextField]()
    ref_text = ft.Ref[ft.TextField]()

    def save_note(e):
        basket.notes.add(
            title = ref_title.current.value,
            note = ref_text.current.value,
        )
        page.go("/")

    return ft.View(
        "/new_note/",
        controls=[
            ft.AppBar(
                title=ft.Text("New Note"),
                actions=[
                    ft.IconButton(
                        ft.icons.SAVE,
                        on_click= save_note
                    ),
                ],),
            ft.TextField(
                ref=ref_title,
                label="Title",
            ),
            ft.TextField(
                ref=ref_text,
                expand=True,
                multiline=True,
                value="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",

            ),

        ],
        scroll="auto"
    )
