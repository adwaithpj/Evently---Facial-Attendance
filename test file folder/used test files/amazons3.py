import boto3
from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv('accessKeyId')
AWS_SECRET_ACCESS_KEY=os.getenv('secretAccessKey')

def download_images(bucket_name, image_names, download_folder):
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


