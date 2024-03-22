import flet as ft
from flet_route import Params, Basket, Routing, path


def LoginView2(page: ft.Page, params: Params, basket: Basket):
    ref_username = ft.Ref[ft.TextField]()
    ref_password = ft.Ref[ft.TextField]()

    def login(e):
        print(ref_username.current.value)
        print(ref_password.current.value)
        print(page.width)
        page.go("/otp")

    image_container = None
    if page.width >= 1200:  # Check if the screen width is large
        image_container = ft.Container(
            content=ft.Image(
                src="assets/svg/login_page.svg"
            ),
        )
    else:
     return ft.View(
        "/",

        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=0,
        controls=[
            ft.Row(
                wrap=False,
                spacing=1,
                controls=[
                    image_container,
                    ft.Container(
                        content=ft.Image(
                            src="assets/svg/login_page.svg"
                        ),
                    ),   # Include the image container here
                    ft.VerticalDivider(width=40, color="white"),
                    ft.Card(
                        elevation=0,
                        color="#ffffff",
                        surface_tint_color="#ffffff",
                        content=ft.Container(
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # Logo
                                    ft.Container(
                                        alignment=ft.Alignment(-0.8, -0.5),
                                        content=ft.Image(
                                            src="assets/Logo/Logo.svg",
                                            width=247,
                                            height=57,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    # Welcome and Login Text
                                    ft.Container(
                                        width=620,
                                        content=ft.Column(
                                            tight=True,
                                            spacing=0,
                                            alignment=ft.Alignment(-0.8, -0.5),
                                            controls=[
                                                ft.Text(
                                                    "Welcome Back",
                                                    font_family="DM Sans Regular",
                                                    size=32,
                                                ),
                                                ft.Text(
                                                    "Login to use the evently Application",
                                                    font_family="DM Sans Regular",
                                                    size=16,
                                                ),
                                            ]
                                        )
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    # Text Fields
                                    ft.TextField(ref=ref_username, label="Username", width=620, height=68,
                                                 text_align="left"),
                                    ft.TextField(ref=ref_password, label="Password", password=True,
                                                 can_reveal_password=True, width=620, height=68),
                                    # Remember me and Forgot password
                                    ft.Row(
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=350,
                                        controls=[
                                            ft.Checkbox(label="Remember me", value=True,
                                                        on_change=lambda e: print("Remember me"),
                                                        label_style=ft.TextStyle(size=16,
                                                                                  font_family="DM Sans Regular")),
                                            ft.Text(
                                                "Forgot Password?",
                                                font_family="DM Sans Regular",
                                                size=16,
                                                color="#2580B7",
                                            ),
                                        ]),
                                    ft.VerticalDivider(width=10, color="white"),
                                    # Login Button
                                    ft.FilledTonalButton(
                                        style=ft.ButtonStyle(
                                            color='white',
                                            animation_duration=100,
                                            bgcolor={
                                                ft.MaterialState.DEFAULT: "#57BAF5",
                                                ft.MaterialState.HOVERED: "#2580B7"
                                            },
                                            surface_tint_color="#FF5C00",
                                            elevation=0,
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                                            },
                                        ),
                                        text="Login",
                                        on_click=login,
                                        width=620,
                                        height=68,
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    ft.Row(
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                "Don't have an Account?",
                                                font_family="DM Sans Regular",
                                                size=16,
                                            ),
                                            ft.Text(
                                                "Register Here",
                                                font_family="DM Sans Regular",
                                                color="#2580B7",
                                                size=16,
                                            ),
                                        ]),
                                    ft.VerticalDivider(width=100, color="white"),
                                ]
                            ),
                            width=756,
                            padding=20,
                            margin=20,
                        )
                    )
                ]
            )
        ]
    )
