import flet as ft
from flet_core import border_radius, margin, padding, Animation
from flet_route import Params, Basket
import time
import requests
import json
import os
from PIL import Image
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('accessKeyId')
AWS_SECRET_ACCESS_KEY = os.getenv('secretAccessKey')
# EVENT_ID = '6607a04f049f48147df56948'
BUCKET_NAME = "evently-data"

global images_name
global user_token, path


class GotoLoadingScreen:
    def __init__(self):
        self.registered_user = {}
        self.loading_pb = None
        self.show_text = None
        self.loading_pr = None

        self.images_name = []
        self.path = None
        self.event_id = ""

    # Registered Users Function starts here

    def check_images(self, no_of_participants, no_of_images_of_participants):
        if no_of_participants == no_of_images_of_participants:
            return True
        else:
            return False

    def count_images_in_folder(self, folder_path):
        image_count = 0
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                with Image.open(file_path) as img:
                    image_count += 1
            except IOError:
                continue
        return image_count

    def get_registered_users(self, event_id, user_token):
        url = f'https://backend.evently.adityachoudhury.com/api/event/registeredUsers/{event_id}'
        headers = {
            'authorization': f'Bearer {user_token}',
        }
        response = requests.get(url=url, headers=headers)
        print(response.raise_for_status())
        reg_data = response.json()


        try:
            no_of_participants = len(reg_data)
        except TypeError:
            return "error_in_downloading_images"
        global images_name, path
        images_name = []
        for i in range(len(reg_data)):
            user_id = reg_data[i]['userId']['_id']
            image_ext = user_id + '.png'
            images_name.append(image_ext)
        print(images_name)

        path = f'assets/Encoding_Images/{event_id}'
        if no_of_participants == 0:
            return "no_images"
        else:
            if not os.path.exists(path):
                os.makedirs(path)
                no_of_images_of_participants = 0
                return "created_folder"
            else:
                print('Folder already exists')
                no_of_images_of_participants = self.count_images_in_folder(path)
                if self.check_images(no_of_participants, no_of_images_of_participants):
                    return "all_images_downloaded"
                else:
                    return "all_images_updated"

    # Registered Users Function ends here

    # Amazon Code starts here
    def download_images(self, bucket_name, image_names, download_folder):
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-south-1'
        )

        for image_name in image_names:
            s3key = f"profile/{image_name}"
            download_path = f"{download_folder}/{image_name}"
            s3.download_file(bucket_name, s3key, download_path)
            print(f"Downloaded {image_name} to {download_path}")

    # Amazon Code ends here

    def view(self, page: ft.Page, params: Params, basket: Basket):



        self.event_id = params.get('event_id')
        print(self.event_id)
        self.loading_pr = ft.ProgressRing(
            visible=True,
            width=30, height=30, stroke_width=3
        )
        self.loading_pb = ft.ProgressBar(
            visible=False,
            width=400
        )

        self.show_text = ft.Text(
            visible=True,
            value='Checking for Encodings'
        )

        def show_loading(e):
            global images_name, user_token, path
            data_taken_from_login = {}
            data_taken_from_login.update(basket.get('response_data'))
            user_token = data_taken_from_login['backendTokens']['token']
            # user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYWYyMDQ0MTkzN2IxODYwYTg3YWQ3Iiwicm9sZSI6ImFkbWluIiwiZW1haWwiOiJhZGl0eWFzdWJoYW0wM0BnbWFpbC5jb20iLCJ2ZXJpZmllZCI6dHJ1ZSwiaWF0IjoxNzExODM0MjQzLCJleHAiOjE3MTE4MzQ4NDN9.bltVxU8_hpAiA06iOa8Qh24xtGZuhJSWNqIsUl3dFzM"
            print('Checking...')
            check_participants_images = self.get_registered_users(self.event_id, user_token)

            if check_participants_images == "created_folder":
                self.images_name = images_name
                self.path = path
                self.show_text.value = 'New Event , Downloading Images'
                self.loading_pr.visible = False
                self.show_text.visible = True
                self.loading_pb.visible = True
                page.update()
                self.download_images(BUCKET_NAME, self.images_name, self.path)
                time.sleep(2)
                self.show_text.value = 'Image Downloaded'
                page.update()
                time.sleep(0.5)
                self.loading_pb.visible = False
                page.update()
                page.go(f'/gotoevent/{self.event_id}/encoding')
            elif check_participants_images == "all_images_downloaded":
                self.show_text.value = 'All Images Downloaded'
                self.show_text.visible = True
                self.loading_pr.visible = False
                self.loading_pb.visible = False
                page.update()
                page.go(f'/gotoevent/{self.event_id}/encoding')
            elif check_participants_images == "all_images_updated":
                self.images_name = images_name
                self.path = path
                self.show_text.value = 'Images Updating, Downloading Images'
                self.loading_pr.visible = False
                self.loading_pb.visible = True
                self.show_text.visible = True
                page.update()
                self.download_images(BUCKET_NAME, self.images_name, self.path)
                time.sleep(2)
                self.show_text.value = 'Image Downloaded'
                page.update()
                time.sleep(1)
                self.loading_pb.visible = False
                page.update()
                page.go(f'/gotoevent/{self.event_id}/encoding')
            elif check_participants_images == "error_in_downloading_images" or "no_images":
                self.show_text.visible = True
                self.show_text.value = 'No participants found'
                page.update()
                self.loading_pr.visible = False
                self.loading_pb.visible = True
                page.update()
                time.sleep(2)
                self.show_text.value = 'Redirecting to dashboard'
                page.update()
                time.sleep(1.6)
                page.go('/dashboardloading')

            else:
                page.go('/dashboard')

        return ft.View(
            f'/gotoevent/{self.event_id}',
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
                            self.show_text,
                            self.loading_pr,
                            self.loading_pb,
                            ft.IconButton(
                                icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                                autofocus=True,
                                on_click=show_loading,
                                on_focus=show_loading
                            )
                        ]
                    )
                )
            ]
        )
