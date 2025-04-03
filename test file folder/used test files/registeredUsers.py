import requests
import json
import os
from PIL import Image
# from amazons3 import download_images
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv('accessKeyId')
AWS_SECRET_ACCESS_KEY=os.getenv('secretAccessKey')
EVENT_ID = '6607a04f049f48147df56948'
BUCKET_NAME = "evently-data"

# class RegisteredUsers:
#     def __init__(self):
#         pass
def check_images(no_of_participants, no_of_images_of_participants):
    if no_of_participants == no_of_images_of_participants:
        return True
    else:
        return False

def count_images_in_folder(folder_path):
    image_count = 0
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            with Image.open(file_path) as img:
                image_count += 1
        except IOError:
            continue
    return image_count


def get_registered_users(event_id,user_token):
    evnt_id = event_id
    print(evnt_id)
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

    images_name = []
    for i in range(len(reg_data)):
        user_id = reg_data[i]['userId']['_id']
        image_ext = user_id + '.png'
        images_name.append(image_ext)
    print(images_name)

    path = f'assets/Encoding_Images/{event_id}'

    if not os.path.exists(path):
        os.makedirs(path)
        no_of_images_of_participants = 0
        return "created_folder",images_name,path
    else:
        print('Folder already exists')
        no_of_images_of_participants = count_images_in_folder(path)
        if check_images(no_of_participants, no_of_images_of_participants):
            return "all_images_downloaded"
        else:
            return "all_images_updated",images_name,path


if __name__ == '__main__':
    dwld_image = get_registered_users()
    if dwld_image == "created_folder_and_downloaded_images":
        print("Folder created and images downloaded return")
    elif dwld_image == "all_images_downloaded":
        print("All images already downloaded return")
    elif dwld_image == "all_images_updated":
        print("All images updated return")
    else:
        print("Error in downloading images return")

