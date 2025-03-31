import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket
import base64
import numpy as np
import cv2
import face_recognition
import pickle
import time
import requests

cap = None
running = True
global studentIDs, event_id, reg_users , headers

reg_users = {}


PICKLED_FILE_PATH = 'assets/EncodedFiles'


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
        page.go('/dashboard')
        return True
    else:
        return True


def get_name_by_id(user_id):
    global reg_users
    for entry in reg_users:
        if entry["userId"]["_id"] == user_id:
            return entry["userId"]["name"]


class Countdown(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.faceCurFrame = []
        self.encodeCurFrame = []
        self.face_match = False
        self.counter = 0
        self.last_attendance_time = 0
        self.student_name = ''

        # pickle variables
        self.encodedList_withIDS = []
        self.encodeListKnown = []
        self.studentIDs = []

        # UI update variables
        self.attendance_area_id = ft.Text(value='', size=30, font_family='DM Sans Bold')
        self.attendance_area_name = ft.Text(value=' ', size=30, font_family='DM Sans Bold')
        self.attendance_area_status = ft.Text('Searching!', size=30, font_family='DM Sans Medium')

        # Attendance camera area
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        self.camera_area = ft.Container(
            col=8,
            width=1000,
            content=ft.Column([
                self.img
            ]
            )
        )
        self.search_icon = ft.Icon(
            name=ft.icons.SEARCH_ROUNDED,
            color=ft.colors.BLUE,
            size=130
        )

        self.green_tick = ft.Icon(
            name=ft.icons.CHECK_CIRCLE_ROUNDED,
            color=ft.colors.GREEN,
            size=130
        )

        self.yellow_tick = ft.Icon(
            name=ft.icons.CHECK_CIRCLE_ROUNDED,
            color=ft.colors.YELLOW,
            size=130
        )

        self.red_cross = ft.Icon(
            name=ft.icons.CANCEL_ROUNDED,
            color=ft.colors.RED,
            size=130
        )

        self.attendance_area_icon = ft.Container(
            content=self.search_icon
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
                            self.attendance_area_icon,
                            ft.Container(
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=25,
                                    controls=[
                                        ft.Text('Name: ', size=30, font_family='DM Sans Medium'),
                                        self.attendance_area_name
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
                                        self.attendance_area_id
                                    ]
                                )
                            ),
                            ft.Container(
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=25,
                                    controls=[
                                        self.attendance_area_status
                                    ]
                                )
                            )

                        ]  # attendance area name and roll number
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

    def did_mount(self):
        self.update_timer()

    def load_pickle(self):
        print('this is load_pickle function')
        try:
            with open(f'{PICKLED_FILE_PATH}/encoded_data_{event_id}.pkl', 'rb') as f:
                self.encodedList_withIDS = pickle.load(f)
                print('Encoded file loaded')  # Comment out -> after testing/if you don't want to print
            self.encodeListKnown, self.studentIDs = self.encodedList_withIDS

        except Exception as e:
            print(f'Error in loading the encoded files: {e}')

    def check_face(self, frame):
        global regs_users
        print('this is check_face function')
        self.load_pickle()
        # print(self.encodeCurFrame)
        # print(self.faceCurFrame)
        for encodeFace, faceLoc in zip(self.encodeCurFrame, self.faceCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
            print(f'this is matches{matches}')
            print(f' this is face dis{faceDis}')

            matchIndex = np.argmin(faceDis)
            print(f' this is face dis{matchIndex}')
            if matches[matchIndex]:
                global studentIDs
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                studentIDs = self.studentIDs[matchIndex]  # check database if the student ID is present
                self.attendance_area_id.value = studentIDs
                self.student_id = studentIDs
                self.student_name = get_name_by_id(studentIDs)
                print(self.student_name)
                self.attendance_area_name.value = self.student_name
                self.page.update()  # have to implement a function here
                print(f'studentID : {studentIDs}')  # Printing the student ID
                self.face_match = True

                print("face matched")
                return self.face_match
            else:
                self.face_match = False
                print('didnt match')
                return self.face_match

    def update_timer(self):
        print('this is update_Timer function')
        global studentIDs
        while running:
            ret, frame = cap.read()
            # print(frame)
            img_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # print(img_frame)
            self.faceCurFrame = face_recognition.face_locations(img_frame)
            print(f'this is faceCurFrame {self.faceCurFrame}')

            # if not ret or frame is None:                    # Check this line if any problems occurs
            #     self.go('/dashboard')

            if len(self.faceCurFrame) == 0:
                self.counter += 1
                # self.attendance_area_icon.content = self.search_icon
                self.attendance_area_status.value = 'Searching'

                self.attendance_area_id.value = ''
                self.attendance_area_name.value = ''
                self.page.update()
                self.attendance_area_icon.content = self.search_icon
                self.update()
                print("Searching")

            elif len(self.faceCurFrame) == 1:
                self.encodeCurFrame = face_recognition.face_encodings(img_frame, self.faceCurFrame)  # changes
                # print(f'this is encodeCurFrame {self.encodeCurFrame}')
                # threading.Thread(target=self.check_face, args=(frame,)).start()
                self.check_face(frame)

            if self.face_match:
                current_time = time.time()
                if 30 >= current_time - self.last_attendance_time >= 3:
                    self.attendance_area_icon.content = self.yellow_tick
                    self.update()

                    self.attendance_area_status.value = 'Attendance alr Done!'
                    self.page.update()

                    print("Attendance already given")

                    self.face_match = False

                    # self.attendance_area_icon.content = self.search_icon
                    self.page.update()
                    self.update()
                else:
                    self.counter = 1
                    self.last_attendance_time = current_time

                    global headers

                    attendance_response = requests.post(
                        f'https://backend.evently.adityachoudhury.com/api/event/mark/{event_id}/{self.student_id}',
                        headers=headers
                    )
                    if attendance_response.status_code == 200:
                        self.attendance_area_icon.content = self.green_tick
                        self.update()

                        self.attendance_area_status.value = 'Attendance Marked'
                        self.page.update()
                        print("Face Matched")
                        # time.sleep(2)

                        # self.attendance_area_icon.content = self.search_icon
                        self.face_match = False
                        self.page.update()
                        self.update()

            else:
                self.attendance_area_icon.content = self.red_cross
                self.update()

                print("Face not Matched")

            _, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = im_b64.decode("utf-8")
            self.update()

    def build(self):
        print('this is build function')
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        self.camera_area = ft.Container(
            col=8,
            width=1000,
            content=ft.Column([
                self.img
            ]
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

        return self.camera_attendance_area


class Facerecognitionscreen:
    # Constructor and Destructor starts here    -->
    def __init__(self):
        self.event_id = ''
        self.event_name = None
        self.event_name_obj = None
        self.toggledarklight = None
        self.report_problem = None
        self.appbar = None
        self.camera_attendance_container = None

    def __del__(self):
        class_name = self.__class__.__name__
        print('Destructor called for :', class_name)

    def view(self, page: ft.Page, params: Params, basket: Basket):

        global reg_users
        data_taken_from_login = {}
        data_taken_from_login.update(basket.get('response_data'))
        user_token = data_taken_from_login['backendTokens']['token']

        global cap, event_id
        if cap is None:
            initialize_camera()

        # Getting values from params and Basket     -->
        self.event_id = params.get_all()["event_id"]
        # self.event_id = '6609419e257ab3e8dc733974'
        event_id = self.event_id
        print(event_id)

        try:
            self.event_name = basket.get('latest_event_route')
            self.event_name = self.event_name["event_name"]
        except Exception as e:
            self.event_name = "Event"
        global headers
        url = f'https://backend.evently.adityachoudhury.com/api/event/registeredUsers/{event_id}'
        headers = {
            "authorization": f"Bearer {user_token}"
        }
        reg_response = requests.get(url=url, headers=headers)
        print(reg_response.raise_for_status())
        reg_users = reg_response.json()
        print(reg_users)

        # Getting values from params and Basket ends here

        # Routing part  starts here         -->
        def change_route(e):
            # self.camera_screen.visible = False
            if release_camera(page):
                page.go('/dashboardloading')

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

        # Camera Attendance Container starts here   -->

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
                    Countdown()

                ]
            )
        )
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
