import flet as ft
from flet_core import border_radius, margin , padding
from flet_route import Params, Basket
import time
import requests
import json

class LoginView:
    def __init__(self):
        self.page_scren = None
        self.login_button = None
        self.count = 0
        self.logo = ft.Image(
            src='assets/Logo/logo.svg',
            width=247,
            height=57,
            fit=ft.ImageFit.CONTAIN,
        )
        self.banner_image = ft.Image(
            src='assets/svg/login_page.svg',
            visible=True,
            width=100,
            height=1010,
            fit=ft.ImageFit.FIT_HEIGHT,
            border_radius=border_radius.only(top_right=20, bottom_right=20)
        )

        self.welcome_text = ft.Text(
            "Welcome Back",
            font_family="DM Sans Regular",
            size=32,
        )
        self.welcome_description = ft.Text(
            "Login to use the evently Application",
            font_family="DM Sans Regular",
            size=16,
        )
        self.count_text = ft.Text(value='0', size=30, color='black')
        self.ref_username = ft.Ref[ft.TextField]()
        self.ref_password = ft.Ref[ft.TextField]()
        self.username_textf = ft.TextField(ref=self.ref_username, label="Username", width=620, height=68, text_align="left")
        self.password_textf= ft.TextField(ref=self.ref_password, label="Password", password=True, can_reveal_password=True, width=620, height=68)   #Add min 8 length
        self.forgot_password = ft.TextButton(
            # left=100,
            text="Forgot Password?",
            visible=True,
            url="https://evently.adityachoudhury.com/forget",
            style=ft.ButtonStyle(
                color="#57BAF5",

            )
        )
        self.login_success = ft.Text(value="Login Succes",visible=False, size=30, color='black',font_family="DM Sans Regular")

        self.backend_api = "https://backend.evently.adityachoudhury.com"
        self.pr = ft.ProgressRing(width=24, height=24, stroke_width = 5,color="#57BAF5",visible=False)
        self.bs = ft.AlertDialog(
            # actions_alignment=ft.MainAxisAlignment.CENTER,
            title=ft.Text("Hello, you!"),
            icon=ft.Icon(name=ft.icons.CHECK_CIRCLE_ROUNDED, color="green", size=20),

        )


    def view(self,page:ft.Page,params:Params,basket:Basket):
        print(self.count_text.value)

        def loading_animation(e):
            self.pr.visible = True
            page.update()
            login(e)



        def login(e):
            # loading_animation(e)
            self.ref_username = ft.Ref[ft.TextField]()
            self.ref_password = ft.Ref[ft.TextField]()
            print(self.username_textf.value)
            print(self.password_textf.value)

            login_route = f"{self.backend_api}/api/auth/login"
            data = json.dumps({
                "email": self.username_textf.value,
                "password": self.password_textf.value
            })
            print(data)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", login_route, headers=headers, data=data)
            response_data_copy = response.json()
            print(response_data_copy)
            basket.response_data = response.json()
            response_status = response.status_code
            if response_status == 200:
                self.login_success.value = "Login Success!"
                # self.login_success.visible = True
                self.bs.title = ft.Text(
                    self.login_success.value+"\nRedirecting to Dashboard",
                    # text_align=,
                    font_family="DM Sans Regular",
                    size=15
                )
                # self.bs.icon =ft.Icon(name=ft.icons.CHECK_CIRCLE_ROUNDED,color="green",size=20),
                page.dialog = self.bs
                self.bs.open = True
                self.pr.visible = False
                page.update()
                time.sleep(3)
                self.username_textf.value = ""
                self.password_textf.value = ""
                self.bs.open = False
                self.bs.visible = False
                self.login_success.visible = False
                page.update()
                page.go('/dashboard')
            elif  response_status == 404:
                self.login_success.value = "User not found"
                self.username_textf.border_color = "#c90000"
                self.bs.title = ft.Text(self.login_success.value,
                    font_family="DM Sans Regular",
                    size=15)
                # self.bs.icon = ft.Icon(name=ft.icons.DO_DISTURB_ROUNDED,color="red",size=30),
                page.dialog = self.bs
                self.bs.open = True
                self.pr.visible = False
                page.update()
                time.sleep(4)
                self.bs.open = False
                self.username_textf.border_color = "black"
                page.update()

            elif response_status == 401:
                self.login_success.value = "Invalid Password"
                self.password_textf.border_color = "#c90000"
                self.bs.title = ft.Text(self.login_success.value,
                    font_family="DM Sans Regular",
                    size=15)
                # self.bs.icon = ft.Icon(name=ft.icons.DO_DISTURB_ROUNDED, color="red", size=30),
                page.dialog = self.bs
                self.bs.open = True
                self.pr.visible = False
                page.update()
                time.sleep(4)
                self.bs.open = False
                self.username_textf.border_color = "black"
                page.update()

            elif response_status == 406:
                self.login_success.value = "Unable to generate sessions"
                self.bs.title = ft.Text(self.login_success.value,
                    font_family="DM Sans Regular",
                    size=15)
                # self.bs.icon = ft.Icon(name=ft.icons.DO_DISTURB_ROUNDED, color="red", size=30),
                page.dialog = self.bs
                self.bs.open = True
                self.pr.visible = False
                page.update()
                time.sleep(4)
                self.bs.open = False
                page.update()
            elif response_status == 500:
                self.login_success.value = "Server Error"
                self.bs.title = ft.Text(self.login_success.value,
                    font_family="DM Sans Regular",
                    size=15)
                # self.bs.icon = ft.Icon(name=ft.icons.DO_DISTURB_ROUNDED, color="red", size=30),
                page.dialog = self.bs
                self.bs.open = True
                self.pr.visible = False
                page.update()
                time.sleep(4)
                self.bs.open = False
                page.update()






        self.login_button = ft.FilledTonalButton(
                                            style=ft.ButtonStyle(
                                                color='white',
                                                animation_duration= 100,
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
                                            on_click=loading_animation,

                                            width=620,
                                            height=68,
                                        )


        return  ft.View(
                '/login',
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # vertical_alignment=ft.MainAxisAlignment.CENTER,
                padding=0,
                spacing=0,
                controls=[
                    ft.ResponsiveRow(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    # width=2500,
                        spacing=100,
                    controls=[
                        ft.Container(
                            self.banner_image,
                            width=1500,
                            alignment=ft.Alignment(-1,0)
                            ,col={"sm": 6, "md": 4, "xl": 5},
                            bgcolor="#F5F5F5",
                            margin=margin.only(right=-250),
                        ),
                        ft.Container(
                            # alignment=ft.Alignment(1,0),

                            # padding=padding.only(left=200),
                            col={"sm": 6, "md": 4, "xl": 6},
                            width=620,
                            expand=False,
                            margin=margin.only(left=250),
                            # bgcolor="#FFFFFF",
                            padding=20,
                            border_radius=25,
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=self.logo
                                    ),
                                    ft.VerticalDivider(width=20, color='white'),
                                    self.welcome_text,
                                    self.welcome_description,
                                    ft.VerticalDivider(width=5, color='white'),
                                    self.username_textf,
                                    self.password_textf,
                                    ft.Container(
                                        padding=0,
                                        content=self.forgot_password,
                                        alignment=ft.Alignment(1, 0),

                                    ),
                                    ft.VerticalDivider(width=5, color='white'),

                                    self.login_button,
                                    self.login_success,
                                    ft.Container(content=self.pr, alignment=ft.Alignment(0, 0), padding=padding.only(top=20)),

                                ],
                            ),

                        )
                    ],
                    ),
                ]
            )