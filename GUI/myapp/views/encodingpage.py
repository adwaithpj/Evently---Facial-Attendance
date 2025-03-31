import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket
import time
import os
import cv2
import face_recognition
import pickle

global image_folder_path, pickled_files_data_path, path_list
path_list = ''
image_folder_path = ''


class EncodingScreen:
    def __init__(self):
        self.checking_text = None
        self.loading_pr = None
        self.event_id = None
        self.imgList = []
        self.studentIds = []
        self.encodingList = []
        self.encodeList = []
        self.encodeList_withIds = []

    def findEncoding(self, imageList):  # Function for encoding the images
        self.encodingList = []

        for img in imageList:
            try:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                self.encodeList.append(encode)
            except Exception as encodingface:
                print(f'Error in encoding the face {encodingface}')

        print('Encoding Completed')  # Comment out the line -> don't want printing
        return self.encodeList

    def _encode_image(self, img):
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            return encode
        except Exception as encodingface:
            print(f'Error in encoding the face: {encodingface}')
            return None

    def load_images(self):
        global image_folder_path, pickled_files_data_path, path_list  # Function for loading images from Images directory
        try:
            for path in path_list:
                try:
                    img_name = os.path.join(image_folder_path, path)
                    self.imgList.append(cv2.imread(img_name))
                    self.studentIds.append(os.path.splitext(path)[0])
                except Exception as e:
                    print(f'Error in loading the image {e}')
        except Exception as e:
            print(f'Error in loading the images {e}')
        print(self.studentIds)  # Comment out the line -> don't want printing

    def pickle_data(self, event_id):
        global image_folder_path, pickled_files_data_path, path_list  # Function for pickling the data with separate event ID
        self.encodeList_withIds = [self.encodeList, self.studentIds]
        try:
            if not os.path.exists(pickled_files_data_path):  # Checking if directory exists
                with open(pickled_files_data_path, 'wb'):
                    print('created')
                    pass

            pickle_file_path = os.path.join(pickled_files_data_path, f'encoded_data_{event_id}.pkl')

            with open(pickle_file_path, 'wb') as f:
                pickle.dump(self.encodeList_withIds, f)
                print(f'Pickled data with event ID {event_id}')  # Comment out the line -> don't want printing
                return True
        except Exception as e:
            print(f'Error in pickling the data: {e}')

    def view(self, page: ft.Page, params: Params, basket: Basket):

        global image_folder_path, pickled_files_data_path, path_list
        self.checking_text = ft.Text(
            visible=True,
            value='Checking for Encodings',
        )
        page.update()
        self.event_id = params.get_all()["event_id"]
        # self.event_id = '6609419e257ab3e8dc733974'
        image_folder_path = f'assets/Encoding_Images/{self.event_id}'
        print(self.event_id)
        image_folder_path = str(image_folder_path)
        pickled_files_data_path = 'assets/EncodedFiles/'
        path_list = os.listdir(image_folder_path)
        self.loading_pr = ft.ProgressBar(
            visible=True,
            width=400
        )
        page.update()
        def check_file_in_folder():
            file_path = os.path.join(pickled_files_data_path, f'encoded_data_{self.event_id}.pkl')
            print(file_path)
            if os.path.exists(file_path):
                return True
            else:
                return False

        def show_loading(e):
            print('Checking...')
            self.checking_text.value = 'Looking For Encoding File'
            page.update()
            time.sleep(1)
            folder_check = check_file_in_folder()
            if folder_check:
                print('File Found')
                self.checking_text.value = 'Encoding File Found'
                self.loading_pr.visible = False
                page.update()
                time.sleep(1)
                page.go(f'/face_recognition/{self.event_id}')
            else:
                print('File Not Found')
                self.checking_text.value = 'Encoding File Not Found,Checking for Images'
                self.loading_pr.visible = True
                page.update()
                time.sleep(1)
                self.checking_text.value = 'Loading Images'
                page.update()
                self.load_images()
                time.sleep(0.6)
                self.checking_text.value = 'Encoding Images'
                page.update()
                self.findEncoding(self.imgList)
                time.sleep(0.6)
                self.checking_text.value = 'Pickling Data'
                page.update()
                self.pickle_data(self.event_id)
                time.sleep(0.6)
                self.checking_text.value = 'Data Pickled, Redirecting to Attendance Windows'
                page.update()
                self.loading_pr.visible = False
                page.update()
                page.go(f'/face_recognition/{self.event_id}')

        return ft.View(
            f'/gotoevent/{self.event_id}/encoding',
            padding=0,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=padding.all(20),
                    alignment=ft.Alignment(0, 1),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            self.checking_text,
                            self.loading_pr,
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
