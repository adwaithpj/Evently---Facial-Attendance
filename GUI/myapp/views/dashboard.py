import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket

import time
import requests
import json



user_token = ''


class Dashboard:
    def __init__(self):
        self.refresh_progressring = None
        self.user_role = None
        self.event_name_to_route = None
        self.logout_progressring = None
        self.sidebar_profile_box = None
        self.upper_dashboard_name = None
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
        self.user_token = " "
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

        # view dashboard variable
        self.table = None
        self.latest_event_card = None
        self.dashboard_analytics_card = None

        # lates event card variables                 #Update this after implementing basket
        self.latest_event_status = ft.Text(
            value="There might be a problem",
            font_family="DM Sans Bold",
            size=25,
        )
        self.latest_event_name = ft.Text(
            value="Refresh the Page",
            font_family="DM Sans Bold",
            size=60
        )
        self.latest_event_description = ft.Text(
            value="There might be a problem with the app, reload please!",
            font_family="DM Sans Regular",
            # color=ft.colors.GREY_300,
            max_lines=3,
            # no_wrap=True,
            size=15.2
        )
        self.latest_event_date = ft.Text(
            text_align=ft.TextAlign.CENTER,

            value="19/03/2024",
            font_family="DM Sans Bold",
            size=20,
            color=ft.colors.BLUE

        )
        self.latest_event_time = ft.Text(
            text_align=ft.TextAlign.CENTER,

            value="2:00pm - 6:00pm",
            font_family="DM Sans Bold",
            size=15,
            color=ft.colors.BLUE
        )
        self.latest_event_attendance_button = ft.FloatingActionButton(
            text='Go to event',
            # autofocus=True,
            icon=ft.icons.ARROW_FORWARD_ROUNDED,
            # on_click= print(params.get())
        )


        self.latest_event_id = None
        self.upcomingdata = []


        # latest event ends here

        # Analytics Variables
        # self.df = px.data.gapminder().query("continent=='Oceania'")
        # self.fig = px.line(self.df, x="year", y="lifeExp", color="country")
        self.linechart = ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(1, 1),
                ft.LineChartDataPoint(3, 1.5),
                ft.LineChartDataPoint(5, 1.4),
                ft.LineChartDataPoint(7, 3.4),
                ft.LineChartDataPoint(10, 2),
                ft.LineChartDataPoint(12, 2.2),
                ft.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=8,
            color=ft.colors.LIGHT_GREEN,
            curved=True,
            stroke_cap_round=True,
        ),



    # Getting Data from API





    # Getting Data from API ends here



    def view(self, page: ft.Page, params: Params, basket: Basket):

        global user_token
        def get_token_data(basket: Basket):
            global user_token
            try:
                self.data_taken_from_login.update(basket.get('response_data'))
                user_token = self.data_taken_from_login['backendTokens']['token']
                print(user_token)
                self.user_refresh_token = self.data_taken_from_login['backendTokens']['refreshToken']
                self.user_id =  self.data_taken_from_login['user']['_id']
                self.user_name =   self.data_taken_from_login['user']['name']
                self.user_email = self.data_taken_from_login['user']['email']
                self.user_role =  self.data_taken_from_login['user']['role']
            except TypeError:
                page.go('/login')

        get_token_data(basket)

        # face recognition route
        def route_face_recognition(e):
            print(self.latest_event_id)
            page.go(f'/gotoevent/{self.latest_event_id}')


        self.latest_event_attendance_button = ft.FloatingActionButton(
            text='Go to event',
            # autofocus=True,
            icon=ft.icons.ARROW_FORWARD_ROUNDED,
            on_click=route_face_recognition
        )



        #face recognition route ends here




        # Routing to loading screen
        # page.go('/loading_screen')
        # Data tables functions
        def get_current_event_data(e, update, data1: dict):
            # global user_token
            # global update_event_name, update_event_date, update_event_time, update_event_desc, update_event_id
            data = data1

            try:

                if len(data[f'{update}']) > 0:
                    print(f"{update} Event ")
                    if update == "today" or update == "tomorrow":
                        self.latest_event_status.value = f"{update.capitalize()}'s Event"
                    elif update == "upcoming":
                        self.latest_event_status.value = f"{update.capitalize()} Event"
                    self.latest_event_name.value = data[f'{update}'][0]['eventName']
                    self.event_name_to_route = data[f'{update}'][0]['eventName']
                    dt_obj = data[f'{update}'][0]['eventStartDate']
                    self.latest_event_date.value, self.latest_event_time.value = dt_obj.split('T')
                    self.latest_event_time.value = self.latest_event_time.value.rstrip('Z')
                    self.latest_event_description.value = data[f'{update}'][0]['eventDescription']
                    self.latest_event_id = data[f'{update}'][0]['_id']
                    params.event_id = self.latest_event_id
                    basket.latest_event_route = {
                        'event_id': self.latest_event_id,
                        'event_name': self.event_name_to_route,
                    }
                    page.update()
                    print(self.latest_event_status.value)  # Comment out this after testing
                    print(self.latest_event_name.value)  # Comment out this after testing
                    print(self.latest_event_time.value)  # Comment out this after testing
                    print(self.latest_event_description.value)  # Comment out this after testing
                    print(self.latest_event_id)  # Comment out this after testing
            except Exception as e:
                print(e)

        def update_table_data(data: list):
            global user_token
            # Data tables variables
            print(data)
            self.table.visible = True
            self.table.rows.clear()
            for event in self.upcomingdata:
                # print(event)
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(event["eventName"])),
                        ft.DataCell(ft.Text(event["eventOwner"])),
                        ft.DataCell(ft.Text(event["eventCategory"]['categoryName'])),
                        ft.DataCell(ft.Text(event["price"])),
                        ft.DataCell(ft.Text(event["eventStartDate"].split('T')[0])),
                        ft.DataCell(ft.Text(event["eventEndDate"].split('T')[0])),
                        ft.DataCell(ft.Text(event["eventParticipationLimit"])),
                        ft.DataCell(ft.Text(event["_id"])),
                        ft.DataCell(ft.IconButton(
                            icon=ft.icons.ARROW_FORWARD_ROUNDED,
                            url=event["_id"],
                        ))
                    ]
                )
                self.table.rows.append(row)
            page.update()

        def check_event(e):
            global user_token
            self.upcomingdata = []
            print(f'this is self.user_token , {user_token}')
            try:
                headers = { 'authorization': f'Bearer {user_token}' }
                url= 'https://backend.evently.adityachoudhury.com/api/event/createdByMe'
                response = requests.get(url=url, headers=headers)
                print(response.status_code)
                data = response.json()
                print(data)
                if len(data['today']) > 0:
                    get_current_event_data(e, update="today", data1=data)
                    self.upcomingdata = data['tomorrow'] + data['upcoming']
                    print(self.upcomingdata)
                elif len(data['tomorrow']) > 0:
                    get_current_event_data(e, update="tomorrow", data1=data)
                    self.upcomingdata = data['upcoming']
                    print(self.upcomingdata)
                elif len(data['upcoming']) > 0:
                    print(data['upcoming'][0])
                    get_current_event_data(e, update="upcoming", data1=data)
                    self.upcomingdata = data['upcoming'][1:len(data['upcoming'])-1]
                    print(self.upcomingdata)
            except Exception as e:
                print(e)
            update_table_data(self.upcomingdata)



        # Data tables variables end here

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
                page.theme_mode = "dark"
                self.logo.color = "white"
            page.update()
            # time.sleep(0.5)
            self.toggledarklight.selected = not self.toggledarklight.selected
            page.update()

        # Button for turning on and off dark and light mode
        self.toggledarklight = ft.IconButton(
            on_click=change_theme,
            # content=ft.Text("Dark Mode",style=ft.TextStyle(color=ft.colors.SURFACE_VARIANT)),
            icon='dark_mode',
            selected_icon='light_mode',
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK, "selected": ft.colors.WHITE}
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

        # Logout Function
        self.logout_progressring = ft.ProgressRing(visible=False, width=16, height=16, stroke_width=2)



        def logout(e):
            self.sidebar_profile_box.visible = False
            self.sidebar_profile_box.open = False
            self.logout_progressring.visible = True
            page.update()

            time.sleep(1)

            page.go('/login')

        # Profile Button
        self.sidebar_profile_box = ft.AlertDialog(
            visible=True,
            open=False,
            content=ft.Container(
                height=300,
                # padding=padding.only(top=20,bottom=20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    # alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=100),
                        ft.Text(
                            value=self.user_name,
                            style=ft.TextStyle(
                                size=25,
                                font_family='DM Sans Bold',
                            )),
                        ft.Text(
                            value=self.user_role,
                            style=ft.TextStyle(
                                size=15,
                                font_family='DM Sans Regular',
                                color=ft.colors.GREY
                            )),
                        ft.VerticalDivider(width=2, thickness=20),
                        ft.IconButton(
                            icon=ft.icons.EDIT_ROUNDED,
                            content=ft.Text("Edit Profile"),
                        ),
                        ft.FloatingActionButton(
                            icon=ft.icons.LOGOUT,
                            # animate_size=Animation(200, "easeOutSine"),
                            text="Logout",
                            on_click=logout
                        ),
                        self.logout_progressring
                    ]
                )
            )
        )

        def open_sidebar_profile(e):
            print("Profile Button Clicked")
            self.sidebar_profile_box.visible = True
            self.sidebar_profile_box.open = True
            page.update()

        self.profile_button = ft.FloatingActionButton(icon=ft.icons.ACCOUNT_CIRCLE, on_click=open_sidebar_profile)
        self.sidebar_profile_name = ft.Text(
            value=self.user_name,
            font_family='DM Sans Bold',
        )
        self.sidebar_email = ft.Text(value=self.user_email, style=ft.TextStyle(color=ft.colors.GREY, size=12))

        # Navigation Routing
        def navigation_routing(e):
            print(e.control.selected_index)
            if e.control.selected_index == 0:
                self.about_us_pagelet.visible = False
                self.contact_us_pagelet.visible = False
                self.dashboard_pagelet.visible = True
                page.update()
            elif e.control.selected_index == 1:
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
                alignment=ft.Alignment(0, 0),
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
                    padding=padding.only(top=-10, bottom=20),

                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.HOME_REPAIR_SERVICE_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.HOME_REPAIR_SERVICE_ROUNDED),
                    label="About US",
                    padding=padding.only(bottom=20),

                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.QUESTION_ANSWER_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.QUESTION_ANSWER_ROUNDED),
                    label_content=ft.Text("Contact Us"),
                    padding=padding.only(bottom=20),

                ),
            ],
            on_change=lambda e: navigation_routing(e),

        )

        # Create button
        self.create_button_text = "Create Event"
        self.create_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, text=self.create_button_text, width=200,
            url='https://evently.adityachoudhury.com/events/create'

        )

        # menu sidebar
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
                        padding=padding.only(top=20, ),
                        alignment=ft.Alignment(-0.85, 0)),

                    self.rail,
                ]
            ),

        )

        # Create Event Container
        self.create_event_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Divider(height=1, thickness=1),
                    ft.VerticalDivider(width=3, thickness=2),
                    self.create_button,
                    ft.VerticalDivider(width=3, thickness=2),
                    ft.Divider(height=1, thickness=1),

                ],
                # alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            ),

            width=250,
        )

        # Dashboard Pagelet variable here
        self.upper_dashboard_name = ft.Text(
            value=f"Welcome, {self.user_name}",
            style=ft.TextStyle(
                size=35,
                font_family='DM Sans Bold',
            ),
            color=ft.colors.INVERSE_SURFACE,
        )

        self.table = ft.DataTable(
            # border=ft.border.all(2, "red"),
            show_bottom_border=True,
            visible=False,
            # columns 里必须添加 DataColumn 类型的控件
            column_spacing=90,
            columns=[
                ft.DataColumn(ft.Text("Event Name")),
                ft.DataColumn(ft.Text("Event Owner")),
                ft.DataColumn(ft.Text("Event Category"), numeric=True),
                ft.DataColumn(ft.Text("Event Price"), numeric=True),
                ft.DataColumn(ft.Text("Event Start Date"), numeric=True),
                ft.DataColumn(ft.Text("Event End Date"), numeric=True),
                ft.DataColumn(ft.Text("Event Participation Limit"), numeric=True),
                ft.DataColumn(ft.Text("Event URL"), numeric=True),
                ft.DataColumn(ft.Text("")),
            ],
            # rows 里必须添加 DataRow 类型的控件
            # DataRow

        )

                                                  # here table updation function
        # Latest event card variables                                                               # latest event card variables

        self.latest_event_card = ft.Card(
            content=ft.Container(
                width=890,
                # bgcolor='grey',
                height=330,
                padding=padding.all(20),
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=650,
                            height=290,
                            # bgcolor='green',
                            content=ft.Column(
                                spacing=0,
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                # tight=True,
                                controls=[
                                    self.latest_event_status,
                                    self.latest_event_name,
                                    ft.Container(
                                        width=500,
                                        content=self.latest_event_description,
                                    ),
                                    ft.Container(
                                        margin=margin.only(top=10),
                                        width=166,
                                        height=37,
                                        padding=padding.only(top=1, bottom=1, left=10, right=10),
                                        alignment=ft.Alignment(0, 0),
                                        border_radius=20,
                                        content=self.latest_event_date,
                                        bgcolor=ft.colors.WHITE
                                    )

                                ]
                            )
                        ),
                        ft.Container(
                            width=190,
                            height=290,
                            padding=padding.only(bottom=20),
                            # bgcolor='blue',
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    ft.Container(
                                        margin=margin.only(top=10),
                                        width=166,
                                        height=37,
                                        padding=padding.only(top=1, bottom=1, left=10, right=10),
                                        alignment=ft.Alignment(0, 0),
                                        border_radius=20,
                                        content=self.latest_event_time,
                                        bgcolor=ft.colors.WHITE
                                    ),
                                    ft.Container(
                                        self.latest_event_attendance_button
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )




        self.dashboard_analytics_card = ft.Card(
            content=ft.Container(
                width=640,
                height=330,
                padding=padding.all(20),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        ft.Text(
                            value='Event Analytics',
                            font_family='DM Sans Bold',
                            size=25,
                        ),
                        ft.Container(
                            height=270,
                            content=ft.Text(
                                value="Still in beta"
                            )
                        )

                    ]
                )
            )
        )

        # scrolling function
        def myscroll(e: ft.OnScrollEvent):
            # e.offset =
            print(
                f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
            )

        check_event(page)
        # Dashboard Pagelet
        self.dashboard_pagelet = ft.Pagelet(
            expand=True,
            visible=True,
            expand_loose=True,
            content=ft.ResponsiveRow(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                columns=1,
                controls=[
                    ft.Container(
                        margin=margin.only(left=44, right=44, top=25, bottom=25),
                        # padding=padding.only(top=70, bottom=100, left=30, right=30),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                            width=page.window_width,
                            spacing=30,
                            scroll=ft.ScrollMode.AUTO,
                            adaptive=True,
                            controls=[
                                ft.Container(
                                    # bgcolor='grey',
                                    content=ft.ResponsiveRow(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Container(
                                                alignment=ft.Alignment(0, 0),
                                                padding=padding.only(left=28, top=34.5, bottom=34.5),
                                                # bgcolor='grey',
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Container(
                                                            width=550,
                                                            height=53,
                                                            content=self.upper_dashboard_name
                                                        ),
                                                        ft.Row(

                                                            controls=[
                                                                ft.Container(

                                                                    content=self.toggledarklight
                                                                ),
                                                                ft.Container(
                                                                    width=215,
                                                                    height=72,
                                                                    # padding=padding.only(right=20),
                                                                    content=ft.FloatingActionButton(
                                                                        # Here updating function goes <--
                                                                        icon=ft.icons.REFRESH_ROUNDED,
                                                                        # offset=ft.Offset(0, 0),
                                                                        # animate_offset=ft.animation.Animation(800, "easeOutSine"),
                                                                        text="Refresh",
                                                                        on_click= check_event,            # When clicking this part
                                                                    )
                                                                ),
                                                            ]
                                                        )

                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    # bgcolor='grey',
                                    expand_loose=True,
                                    content=ft.ResponsiveRow(
                                        alignment=ft.MainAxisAlignment.CENTER,

                                        controls=[
                                            ft.Container(

                                                content=ft.Row(
                                                    scroll=ft.ScrollMode.AUTO,
                                                    on_scroll=myscroll,
                                                    # auto_scroll=True,
                                                    animate_opacity=ft.animation.Animation(400),
                                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                    spacing=100,
                                                    controls=[
                                                        self.latest_event_card,
                                                        self.dashboard_analytics_card

                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    # bgcolor='grey',
                                    expand_loose=True,
                                    content=ft.ResponsiveRow(
                                        alignment=ft.MainAxisAlignment.CENTER,

                                        controls=[
                                            ft.Column(
                                                controls=[
                                                    ft.Text(
                                                        value='Upcoming Event',
                                                        font_family='DM Sans Bold',
                                                        size=25,
                                                    )
                                                ]
                                            ),
                                            ft.Container(
                                                # bgcolor='grey',
                                                expand_loose=True,
                                                content=ft.Row(
                                                    scroll=ft.ScrollMode.AUTO,
                                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                    controls=[
                                                        self.table,

                                                    ]
                                                )

                                            )  # above is the data table - this is dummy data
                                        ]
                                    )
                                )
                            ]
                        ),
                    )
                ]
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
                        padding=padding.only(top=70, bottom=100, left=30, right=30),
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
                                    padding=padding.only(left=100, right=100),
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
            expand_loose=True,
            # padding=padding.only(top=55, bottom=20),
            content=ft.ResponsiveRow(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                columns=1,
                spacing=60,
                # run_spacing=100,
                controls=[
                    ft.Container(
                        padding=padding.only(top=70, bottom=100, left=30, right=30),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            width=page.window_width,
                            height=830,
                            spacing=40,
                            scroll=ft.ScrollMode.ALWAYS,
                            adaptive=True,
                            controls=[
                                ft.Text(
                                    text_align=ft.TextAlign.CENTER,
                                    size=70,
                                    font_family="Circular Spotify Tx T",
                                    value="Contact Us",
                                ),
                                ft.Text(
                                    value='For any queries or feedback, feel free to reach out to us at:',
                                    size=25,
                                    weight=ft.FontWeight.NORMAL,
                                    font_family="DM Sans Medium",
                                ),
                                ft.Container(
                                    content=ft.ResponsiveRow(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Container(
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Card(
                                                            content=ft.Container(
                                                                width=400,
                                                                padding=padding.all(20),
                                                                content=ft.Column(
                                                                    controls=[
                                                                        ft.ListTile(
                                                                            leading=ft.Icon(ft.icons.EMAIL,
                                                                                            tooltip='Email'),
                                                                            title=ft.Text(
                                                                                value='Email',
                                                                                weight=ft.FontWeight.BOLD,
                                                                                font_family="DM Sans Medium",
                                                                            ),
                                                                            subtitle=ft.Text(
                                                                                'Contact us through email, click the button below')
                                                                        ),
                                                                        ft.Row(
                                                                            controls=[

                                                                                ft.IconButton(
                                                                                    ft.icons.ARROW_FORWARD_ROUNDED,
                                                                                    url="mailto:adwaithleans616@gmail.com?subject=Me&body=Hello!")
                                                                            ],
                                                                            alignment=ft.MainAxisAlignment.END,
                                                                        ),
                                                                    ]
                                                                )
                                                            )
                                                        ),
                                                        ft.Card(
                                                            content=ft.Container(
                                                                width=400,
                                                                padding=padding.all(20),
                                                                content=ft.Column(
                                                                    controls=[
                                                                        ft.ListTile(
                                                                            leading=ft.CircleAvatar(
                                                                                foreground_image_url="https://img.freepik.com/free-vector/new-2023-twitter-logo-x-icon-design_1017-45418.jpg?w=740&t=st=1711190750~exp=1711191350~hmac=e73e78691ab631f9f74f59cc73fdb1062e7e1331209543b7e775b4fbc82b5e7c",
                                                                            ),
                                                                            title=ft.Text(
                                                                                value='X',
                                                                                weight=ft.FontWeight.BOLD,
                                                                                font_family="DM Sans Medium",
                                                                            ),
                                                                            subtitle=ft.Text(
                                                                                'Contact us through Twitter, click the button below')
                                                                        ),
                                                                        ft.Row(
                                                                            controls=[

                                                                                ft.IconButton(
                                                                                    ft.icons.ARROW_FORWARD_ROUNDED,
                                                                                    url="https://twitter.com/AdwaithPj")
                                                                            ],
                                                                            alignment=ft.MainAxisAlignment.END,
                                                                        ),
                                                                    ]
                                                                )
                                                            )
                                                        ),

                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
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
                self.sidebar_profile_box,
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
                                    ft.VerticalDivider(width=10, thickness=20, color='black'),
                                    self.create_event_container,
                                    self.menu_sidebar,

                                ],
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=280,
                            padding=padding.only(top=55, bottom=20),

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
