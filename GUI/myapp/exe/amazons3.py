import boto3
from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv('accessKeyId')
AWS_SECRET_ACCESS_KEY=os.getenv('secretAccessKey')

# class Amazons3ImagesDWLD:
#     def __init__(self):
#         pass

def download_images(self,bucket_name, image_names, download_folder):
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







# Usage example
# bucket_name = "evently-data"
# image_names = ["65b5fcf613bb3b7a22ed78bd.png","65b9cfc48737feb8879a4ffc.png","65bcc23eb4245f4558f36342.png"]
# download_folder = "assets/Encoding_Images/FirstEvent"


# download_images(bucket_name, image_names, download_folder)
