import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket
import base64
import cv2

cap = None
running = True


def initialize_camera():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)


def release_camera(page):
    global cap, running
    running = False
    if cap is not None:
        cap.release()
        cap = None

        cv2.destroyAllWindows()
        running = True
        page.go('/loading_screen')
        return True
    else:
        return True


class Countdown(ft.UserControl):
    def __init__(self):
        super().__init__()

    def did_mount(self):
        self.update_timer()

    def update_timer(self):
        global cap, running
        while running:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            _, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = im_b64.decode("utf-8")
            self.update()

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        return self.img


class Facerecognitionscreen():

    # Constructor and Destructor starts here    -->
    def __init__(self):
        super().__init__()
        self.red_cross = None
        self.green_tick = None
        self.camera_attendance_container = None
        self.appbar = None
        self.attendance_area = None
        self.camera_area = None
        self.camera_attendance_area = None
        self.report_problem = None
        self.toggledarklight = None
        self.event_name = None
        self.event_id = None
        self.event_name_obj = None
        self.running = True
        self.should_run = True

    def __del__(self):
        class_name = self.__class__.__name__

        print('Destructor called for :', class_name)

    # Constructor and Destructor ends here

    # Flet view function starts here    -->
    def view(self, page: ft.Page, params: Params, basket: Basket):

        global cap
        if cap is None:
            initialize_camera()

        # Getting values from params and Basket     -->
        self.event_id = params.get_all()["event_id"]
        try:
            self.event_name = basket.get('latest_event_route')
            self.event_name = self.event_name["event_name"]
        except Exception as e:
            self.event_name = "Event"

        # self.event_name = "Event 1"
        # self.event_id = "22322323"
        # Getting values from params and Basket ends here

        # Routing part  starts here         -->

        def change_route(e):
            # self.camera_screen.visible = False
            if release_camera(page):
                page.go('/loading_screen')

        # Routing part ends here

        # Appbar variables start here     -->

        self.event_name_obj = ft.Text(
            value=self.event_name,
            size=30,
            font_family='DM Sans Bold',
        )

        def change_theme(e):  # function for dark and light mode
            if page.theme_mode == "dark":
                page.theme_mode = "light"
            else:
                page.theme_mode = "dark"

            page.update()
            # time.sleep(0.5)
            self.toggledarklight.selected = not self.toggledarklight.selected
            page.update()

        self.toggledarklight = ft.IconButton(
            # style=ft.ButtonStyle(
            #     color={"": ft.colors.BLACK, "selected": ft.colors.WHITE}
            # ),
            on_click=change_theme,
            icon='dark_mode',
            selected_icon='light_mode',
            icon_size=25,

        )

        self.report_problem = ft.IconButton(
            icon=ft.icons.REPORT,
            icon_size=25,
            url='https://x.com/AdwaithPj'
        )

        self.appbar = ft.AppBar(
            title=self.event_name_obj,
            leading=ft.IconButton(
                ft.icons.ARROW_BACK,
                on_click=change_route),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            toolbar_height=70,
            actions=[
                self.toggledarklight,
                self.report_problem
            ],

            leading_width=80
        )
        # Appbar variables ends here

        # Camera Attendance Area starts here        -->
        self.camera_area = ft.Container(
            col=8,
            width=1000,
            content=ft.Column([
                Countdown(),
                # ft.Text('camera')
            ]
            )
        )

        self.green_tick = ft.Icon(
            name=ft.icons.CHECK_CIRCLE_ROUNDED,
            color=ft.colors.GREEN,
            size=130
        )
        self.red_cross = ft.Icon(
            name=ft.icons.CANCEL_ROUNDED,
            color=ft.colors.RED,
            size=130
        )

        self.attendance_area = ft.Container(
            col=4,
            # bgcolor='blue',
            width=620,
            content=ft.Card(
                height=450,
                content=ft.Container(
                    alignment=ft.Alignment(0, 1),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                        controls=[
                            ft.Container(self.green_tick),
                            ft.Container(
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=25,
                                    controls=[
                                        ft.Text('Name: ',size=30,font_family='DM Sans Medium'),
                                        ft.Text('Adwaith P J',size=30,font_family='DM Sans Bold')
                                    ]
                                )
                            ),
                            ft.Container(
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=25,
                                    controls=[
                                        ft.Text('ID: ', size=30, font_family='DM Sans Medium'),
                                        ft.Text('22jdsi1212121', size=30, font_family='DM Sans Bold')
                                    ]
                                )
                            ),
                            ft.Container(
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=25,
                                    controls=[
                                        ft.Text('Attendance Done! ', size=30, font_family='DM Sans Medium'),
                                    ]
                                )
                            )

                        ]
                    )
                )
            )
        )

        self.camera_attendance_area = ft.Container(
            padding=padding.only(left=30, right=30, top=30, bottom=30),
            content=ft.ResponsiveRow(
                controls=[
                    self.camera_area,
                    self.attendance_area
                ]
            )
        )

        self.camera_attendance_container = ft.Container(
            alignment=ft.Alignment(0, 1),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=padding.only(top=26, bottom=26),
                        content=ft.Text(
                            value="Please Look into the camera!",
                            size=26,
                            font_family='DM Sans Medium',
                        )
                    ),
                    self.camera_attendance_area

                ]
            )
        )
        # Camera and attendance ends here

        # Return part starts here   -->

        return ft.View(
            route=f'/face_recognition/{self.event_id}',
            # route='/face_recognition/1',
            controls=[
                self.appbar,
                self.camera_attendance_container
            ]
        )

        # Return part ends here

        # Flet  view function ends here
