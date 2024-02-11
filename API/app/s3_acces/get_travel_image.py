#!/usr/bin/env python3

import boto3, requests, aioboto3
from ..security.enviroment import env_variable
import aiohttp
import aioboto3

class FilesAWSS3():
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
        self.uploaded_keys = []

    def upload_image(self, image_path: str):
        path = f"travels_images/{image_path}"
        pass
    
    async def upload_airpline_logo(self, image_url, image_name: str):
        # Ensure the image_name ends with .png
        if not image_name.lower().endswith('.png'):
            image_name += '.png'

        key = f"static_images/airline_logos/{image_name}"

        # Create an aiohttp session for downloading the image
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                try:
                    response.raise_for_status()  # Check if the response is successful
                    image_content = await response.read()  # Read the image content as bytes
                    
                    # Use aioboto3 to upload the image content to S3 asynchronously
                    async with aioboto3.client('s3',
                                            aws_access_key_id=self.acces_key,
                                            aws_secret_access_key=self.secret_acces_key) as s3_client:
                        await s3_client.put_object(
                            Bucket=self.static_images_bucket_name,
                            Key=key,
                            Body=image_content,
                            ContentType='image/png'  # Set the ContentType to image/png
                        )
                        print(f"Image {image_name} uploaded as PNG")
                        # Return the URL of the uploaded image
                        return f"https://{self.static_images_bucket_name}.s3.{self.region_name}.amazonaws.com/{key}"
                except aiohttp.ClientResponseError as e:
                    print(f"Failed to download image from {image_url} - HTTP status code: {response.status}")
                    return None
                except Exception as e:
                    print(f"Failed to upload image {image_name} to S3: {e}")
                    return None
          


    def get_uploaded_images_urls(self):
        """Generates URLs for all uploaded images."""
        base_url = f"https://{self.static_images_bucket_name}.s3.{self.region_name}.amazonaws.com"
        return [f"{base_url}/{key}" for key in self.uploaded_keys]



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

    def extract_airline_photo(airline):
        key = ""
        pass

if __name__ == "__main__":
    S3_Handler = FilesAWSS3()

    image_ogigin_url = "https://airlinelogos.net//albums/g/thumb_garudaindonesian-white.gif"
    image_name = "Gator_GlobalFlying_Services"
    
    S3_Handler.upload_airpline_logo(image_ogigin_url, image_name)
    