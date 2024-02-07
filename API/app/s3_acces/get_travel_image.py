#!/usr/bin/env python3

import boto3
from ..security.enviroment import env_variable



class ImagesHandleS3():
    """
     *add description about this class here*
    """
    def __init__(self):
        self.acces_key = env_variable["AWS_ACCES_KEY"]
        self.secret_acces_key = env_variable["AWS_SECRET_ACCES_KEY"]
        self.static_images_bucket_name = "travel360-images-handle"
        self.client_s3 = boto3.client(
            's3',  # Remove leading spaces here
            aws_access_key_id=self.acces_key,
            aws_secret_access_key=self.secret_acces_key
        )

    def load_image(self, image_path: str):
        path = f"travels_images/{image_path}"
        pass

    def load_image_obj(self, image: bytes):
        pass

    def get_image(self, image_name):
        key = f"/travels_images/{image_name}"

        try:
            response = self.client_s3.get_object(
                Bucket=self.static_images_bucket_name,
                Key=key
            )
            return response['Body'].read()  # You need to call read() to get the bytes of the file
        except self.client_s3.exceptions.NoSuchKey:
            print(f"Image not found: {image_name}")
            return None
        except Exception as e:
            print(f"An error occurred downloading the image: {e}")
            raise Exception(e)

if __name__ == "__main__":
    # Testing part
    print(env_variable["AWS_ACCES_KEY"])
    print(env_variable["AWS_SECRET_ACCES_KEY"])
