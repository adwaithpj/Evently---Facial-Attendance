import flet as ft
from flet_core import border_radius, margin , padding, Animation
from flet_route import Params, Basket
import time
import requests
import json



class Dashboard:
    def __init__(self):
        self.main_body = None
        self.nav_check = None
        self.contact_us_pagelet = None
        self.about_us_pagelet = None
        self.dashboard_pagelet = None
        self.create_event_container = None
        self.menu_sidebar = None
        self.sidebar_email = None
        self.sidebar_profile_name = None
        self.profile_button = None
        self.create_button = None
        self.create_button_text = None
        self.user_token = None
        self.user_refresh_token = None
        self.user_id = None
        self.user_name = None
        self.user_email = None
        self.data_taken_from_login = {}
        self.page_appbar = None
        self.navigation_destination = None

        # self.navigation_destination = ft.Text("Dashboard")

        # view variable
        self.toggledarklight = None
        self.rail = None
        self.logo = ft.Image(

            src='assets/Logo/logo.svg',
            width=237,
            height=47,
            # color="black",
            fit=ft.ImageFit.FIT_WIDTH,
        )

    # def get_token_data(self,basket: Basket):
    #     self.data_taken_from_login.update(basket.get('response_data'))
    #     self.user_token = self.data_taken_from_login['backendTokens']['token']
    #     self.user_refresh_token = self.data_taken_from_login['backendTokens']['refreshToken']
    #     self.user_id =  self.data_taken_from_login['user']['_id']
    #     self.user_name = self.data_taken_from_login['user']['name']
    #     self.user_email = self.data_taken_from_login['user']['email']

    def view(self, page: ft.Page, params: Params, basket: Basket):
        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()
        # self.navigation_destination = self.dashboard_pagelet
        # dark and white theme changing function
        def change_theme(e):
            if page.theme_mode == "dark":
                page.theme_mode = "light"
                self.logo.color = ""
            else:
                page.theme_mode =    "dark"
                self.logo.color = "white"
            page.update()
            # time.sleep(0.5)
            self.toggledarklight.selected = not self.toggledarklight.selected
            page.update()

        #Button for turning on and off dark and light mode
        self.toggledarklight = ft.IconButton(
            on_click= change_theme,
            icon='dark_mode',
            selected_icon='light_mode',
            style=ft.ButtonStyle(
                color={"":ft.colors.BLACK,"selected":ft.colors.WHITE}
            )
        )

        # Page AppBar
        self.page_appbar = ft.AppBar(
                # leading=ft.Icon(ft.icons.PALETTE),
                leading_width=60,
                # title=self.logo,
                center_title=False,
                bgcolor=ft.colors.SURFACE,
                adaptive=True,
                actions=[
                    self.toggledarklight,

                ],
            )

        # Profile Button
        self.profile_button = ft.FloatingActionButton(icon=ft.icons.ACCOUNT_CIRCLE,)
        self.sidebar_profile_name = ft.Text("Adwaith PJ",)
        self.sidebar_email = ft.Text('adwaithleans616@gmail.com',style=ft.TextStyle(color=ft.colors.GREY,size=12))

        #Navigation Routing
        def navigation_routing(e):
            print(e.control.selected_index)
            if e.control.selected_index == 0:
                self.about_us_pagelet.visible = False
                self.contact_us_pagelet.visible = False
                self.dashboard_pagelet.visible = True
                page.update()
            elif e.control.selected_index ==1:
                self.about_us_pagelet.visible = True
                self.contact_us_pagelet.visible = False
                self.dashboard_pagelet.visible = False
                page.update()
            elif e.control.selected_index == 2:
                self.about_us_pagelet.visible = False
                self.contact_us_pagelet.visible = True
                self.dashboard_pagelet.visible = False
                page.update()


        # Navigation Rail
        self.rail = ft.NavigationRail(

            selected_index=0,
            label_type=None,
            min_width=90,
            min_extended_width=100,
            expand=True,
            extended=True,
            indicator_shape=ft.ContinuousRectangleBorder(radius=20),
            trailing=ft.Container(
                # bgcolor='grey',
                padding=padding.only(top=360),
                alignment=ft.Alignment(0,0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[

                        self.profile_button,
                        self.sidebar_profile_name,
                        self.sidebar_email,
                    ]
                )
            ),
            group_alignment=-0.9,
            destinations=[
                # ft.VerticalDivider(width=5,thickness=20,color='black'),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.DASHBOARD_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.DASHBOARD_ROUNDED),
                    label="Dashboard",
                    padding=padding.only(top=-10,bottom=20),

                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.HOME_REPAIR_SERVICE_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.HOME_REPAIR_SERVICE_ROUNDED),
                    label="About US",
                    padding=padding.only( bottom=20),


                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.QUESTION_ANSWER_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.QUESTION_ANSWER_ROUNDED),
                    label_content=ft.Text("Contact Us"),
                    padding=padding.only( bottom=20),

                ),
            ],
            on_change=lambda e: navigation_routing(e),


        )

        # Create button
        self.create_button_text = "Create Event"
        self.create_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, text=self.create_button_text,width=200,
            url='https://evently.adityachoudhury.com/events/create'


        )

        #menu sidebar
        self.menu_sidebar = ft.Container(
                                        expand=True,
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    content=ft.Text(
                                                        "Menu",
                                                        style=ft.TextStyle(
                                                            size=20,
                                                            font_family='DM Sans Medium',
                                                        )),
                                                    padding=padding.only(top=20,),
                                                    alignment=ft.Alignment(-0.85,0)),

                                            self.rail,
                                            ]
                                        ),

                                    )

        # Create Event Container
        self.create_event_container = ft.Container(
                                        content=ft.Column(
                                            controls = [
                                                ft.Divider(height=1,thickness=1),
                                                ft.VerticalDivider(width=3,thickness=2),
                                                self.create_button,
                                                ft.VerticalDivider(width=3, thickness=2),
                                                ft.Divider(height=1, thickness=1),

                                            ],
                                            # alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                                        ),

                                        width=250,
                                    )

        # Dashboard Pagelet
        self.dashboard_pagelet = ft.Pagelet(
            expand=True,
            content=ft.Container(
                visible=True,
                content=ft.Column([ft.Text("Dashboard!")], alignment=ft.MainAxisAlignment.START,
                                  expand=True),
                padding=padding.only(top=55, bottom=20),
                bgcolor='grey',
            )

        )

        self.about_us_pagelet = ft.Pagelet(
            expand=True,
            visible=False,

            expand_loose=True,

            # padding=padding.only(top=55, bottom=20),
            content=ft.ResponsiveRow(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                columns=1,
                spacing=60,
                # run_spacing=30,
                controls=[
                    ft.Container(
                        # bgcolor='grey',
                        padding=padding.only(top=70,bottom=100,left=30,right=30),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            width=page.window_width,
                            height=830,
                            spacing=40,
                            scroll=ft.ScrollMode.ALWAYS,
                            adaptive=True,
                            # animate_offset=ft.animation.Animation(400,"easeOutSine"),
                            controls=[
                                ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    size=70,
                                    font_family="Circular Spotify Tx T",
                                    value="About Evently",
                                ),
                                ft.Container(
                                    padding=padding.only(left=100,right=100),
                                    content=ft.Text(
                                        value="Welcome to Evently, where we revolutionize event management with cutting-edge technology and a passion for sustainability! 🌟",
                                        style=ft.TextStyle(
                                            font_family='DM Sans Italic',
                                            size=29,
                                        ),
                                        text_align=ft.TextAlign.CENTER,

                                    )
                                ),
                                ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    size=35,
                                    font_family="Circular Spotify Tx T",
                                    value="Our Mission",
                                ),
                                ft.Container(
                                    padding=padding.only(left=100, right=100),
                                    content=ft.Text(

                                        value='At Evently, our mission is clear: to make event planning smoother, faster, '
                                              'and more eco-friendly. We are committed to reducing paper waste and carbon emissions by offering a digital solution that simplifies event management while minimizing the impact on our planet. 🌍♻️',
                                        style=ft.TextStyle(
                                            font_family='DM Sans Italic',
                                            size=29,
                                        ),
                                        text_align=ft.TextAlign.CENTER,

                                    )
                                ),
                                ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    size=35,
                                    font_family="Circular Spotify Tx T",
                                    value="What We Do",
                                ),
                                ft.Container(
                                    padding=padding.only(left=100, right=100),
                                    content=ft.Text(

                                        value='Evently provides a seamless platform for event organizers to create, manage, '
                                              'and host events with ease. From fast face recognition for check-ins to real-time '
                                              'updates on event performance, we strive to empower organizers and attendees alike.',
                                        style=ft.TextStyle(
                                            font_family='DM Sans Italic',
                                            size=29,
                                        ),
                                        text_align=ft.TextAlign.CENTER,

                                    )
                                ),
                                ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    size=35,
                                    font_family="Circular Spotify Tx T",
                                    value="Our Team",
                                ),
                                ft.Container(

                                    padding=padding.only(left=100, right=100),
                                    content=ft.Text(

                                        value='Evently is brought to you by a dedicated team of innovators, tech enthusiasts, and sustainability advocates.'
                                              ' We believe in the power of technology to make positive change, and were excited to share our passion with you.',

                                        style=ft.TextStyle(
                                            font_family='DM Sans Italic',
                                            size=29,
                                        ),
                                        text_align=ft.TextAlign.CENTER,

                                    )
                                ),
                                ft.Container(
                                    content=ft.ResponsiveRow(
                                        alignment=ft.MainAxisAlignment.CENTER,

                                        controls=[
                                            ft.Container(
                                                # bgcolor='black',
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                    controls=[

                                                        ft.Container(
                                                            content=ft.Column(
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Image(
                                                                        src='assets/about_us_team/adwaith.jpg',
                                                                        width=200,
                                                                        height=200,
                                                                        border_radius=border_radius.all(50),
                                                                        fit=ft.ImageFit.FIT_WIDTH,
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='Adwaith PJ',
                                                                        size=16,
                                                                        font_family='DM Sans Bold Italic',
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='2129013',
                                                                        size=13,
                                                                        font_family='DM Sans Bold Italic',
                                                                    )


                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            content=ft.Column(
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Image(
                                                                        src='assets/about_us_team/aditya11.jpg',
                                                                        width=200,
                                                                        height=200,
                                                                        border_radius=border_radius.all(50),
                                                                        fit=ft.ImageFit.FIT_WIDTH,
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='Aditya Choudhury',
                                                                        size=16,
                                                                        font_family='DM Sans Bold Italic',
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='2129011',
                                                                        size=13,
                                                                        font_family='DM Sans Bold Italic',
                                                                    )

                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            content=ft.Column(
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Image(
                                                                        src='assets/about_us_team/aditya10.jpg',
                                                                        width=200,
                                                                        height=200,
                                                                        border_radius=border_radius.all(50),
                                                                        fit=ft.ImageFit.FIT_WIDTH,
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='Aditya kumar Singh',
                                                                        size=16,
                                                                        font_family='DM Sans Bold Italic',
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='2129010',
                                                                        size=13,
                                                                        font_family='DM Sans Bold Italic',
                                                                    )

                                                                ]
                                                            )
                                                        )
                                                    ]
                                                )
                                            )

                                        ]
                                    )
                                ),
                                ft.Container(
                                    content=ft.ResponsiveRow(
                                        alignment=ft.MainAxisAlignment.CENTER,

                                        controls=[
                                            ft.Container(
                                                # bgcolor='black',
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                    spacing=20,
                                                    controls=[

                                                        ft.Container(
                                                            content=ft.Column(
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Image(
                                                                        src='assets/about_us_team/megha.jpg',
                                                                        width=200,
                                                                        height=200,
                                                                        border_radius=border_radius.all(50),
                                                                        fit=ft.ImageFit.FIT_WIDTH,
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='Megha Varshini',
                                                                        size=16,
                                                                        font_family='DM Sans Bold Italic',
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='2129154',
                                                                        size=13,
                                                                        font_family='DM Sans Bold Italic',
                                                                    )

                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            content=ft.Column(
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Image(
                                                                        src='assets/about_us_team/diptangshu.jpg',
                                                                        width=200,
                                                                        height=200,
                                                                        border_radius=border_radius.all(50),
                                                                        fit=ft.ImageFit.FIT_WIDTH,
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='Diptangshu Bhattacherjee',
                                                                        size=16,
                                                                        font_family='DM Sans Bold Italic',
                                                                    ),
                                                                    ft.Text(
                                                                        text_align=ft.TextAlign.CENTER,
                                                                        value='2129023',
                                                                        size=13,
                                                                        font_family='DM Sans Bold Italic',
                                                                    )

                                                                ]
                                                            )
                                                        )
                                                    ]
                                                )
                                            )

                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )

        )

        self.contact_us_pagelet = ft.Pagelet(
            visible=False,
            expand=True,
            # padding=padding.only(top=55, bottom=20),
            content=ft.ResponsiveRow(

                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                columns=1,
                spacing=40,
                run_spacing=100,
                controls=[
                    ft.Container(
                        padding=padding.only(top=70),
                        content=ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            size=70,
                            font_family="Circular Spotify Tx T",
                            value="Contact Us",
                        ),
                    ),
                    ft.Container(
                        alignment=ft.Alignment(0,0),
                        content=ft.Text("Column 1"),
                        padding=15,
                        bgcolor="grey",
                        col={"sm": 6, "md": 4, "xl": 2},
                    ),

                ]
            )

        )



        return ft.View(
            '/dashboard',
            padding=0,
            spacing=0,
            controls=[
                # self.page_appbar,
                ft.Row(
                    # spacing=48,

                    # width=page.window_width,
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.logo,
                                    ft.VerticalDivider(width=10,thickness=20,color='black'),
                                    self.create_event_container,
                                    self.menu_sidebar,

                                ],
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=280,
                            padding=padding.only(top=55,bottom=20),

                        ),
                        ft.VerticalDivider(width=1),
                        # ft.Container(expand=True,width=200),
                        self.dashboard_pagelet,
                        self.about_us_pagelet,
                        self.contact_us_pagelet

                    ],

                )
            ]
        )