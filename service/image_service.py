# service/image_service.py
import os
import traceback
import uuid
from typing import List

from fastapi import requests
from openai import OpenAI
import requests
from fastapi.responses import FileResponse
from urllib.parse import urlparse
import os


from core.models import ImageDetail, ImageDetailCreate
from core.exceptions import RecordNotFoundError, ImageException
from data.image_repository import ImageRepository
from service.image_service_interface import ImageServiceInterface
from data import get_current_db_context, DatabaseContext

def extract_filename_from_url(url):
    # Parse the URL into components
    url_path = urlparse(url).path

    # Extract the filename from the path
    filename = os.path.basename(url_path)

    return filename

def save_image_from_url(image_url):
    # Get the image from the URL
    response = requests.get(image_url)

    # Extract the filename from the URL
    filename = extract_filename_from_url(image_url)
    filePath = os.path.join(r"image/", filename)

    print("Saving image to", filePath)
    # Open a file in write mode and save the image to it
    with open(filePath, 'wb') as file:
        file.write(response.content)

    return filename
class ImageService(ImageServiceInterface):
    def create_image(self, image_create: ImageDetailCreate) -> ImageDetail:
        print("i am working")
        with DatabaseContext() as db:
            try:
                db.begin_transaction()

                # Generate a unique GUID for the new image
                guid = str(uuid.uuid4())

                # Use the DALL·E API to generate an image from the provided prompt
                ##write image generation code here
                client = OpenAI(base_url='http://aitools.cs.vt.edu:7860/openai/v1', api_key='aitools')
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_create.prompt,
                    style="natural",
                    quality="hd",
                    size="1024x1024",
                    timeout=100
                )
                image_url = response.data[0].url
                image_path = save_image_from_url(image_url=image_url)

                # Create an instance of ImageDetail with the generated GUID, filename, and the original prompt
                image = ImageDetail(guid=guid, filename=image_path, prompt=image_create.prompt)

                # Use the ImageRepository to save the image details to the database
                image_repo = ImageRepository()
                image_repo.create(image)

                db.commit_transaction()
                return image
            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e

    def get_image_by_guid(self, guid: str) -> ImageDetail:
        print("i am working")
        with DatabaseContext() as db:
            try:
                db.begin_transaction()

                # Use the ImageRepository to get the image details from the database
                image_repo = ImageRepository()
                image = image_repo.get_by_guid(guid)

                db.commit_transaction()
                return image

            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e

    def get_all_images(self) -> List[ImageDetail]:
        print("i am working")
        with DatabaseContext() as db:
            try:
                db.begin_transaction()

                # Use the ImageRepository to get all the image details from the database
                image_repo = ImageRepository()
                images = image_repo.get_all()

                db.commit_transaction()
                return images

            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e

    def get_image_content(self, guid: str) -> bytes:
        print("i am get_image_content")
        with DatabaseContext() as db:
            try:
                db.begin_transaction()

                # Use the ImageRepository to get the image details from the database
                image_repo = ImageRepository()
                image = image_repo.get_by_guid(guid)
                image_path = "image/"+image.filename

                # Open the image file and read its content
                with open(image_path, 'rb') as f:
                    image_content = f.read()

                db.commit_transaction()
                # print(image_content)
                return image_content
                # return FileResponse(image_path, media_type='image/jpeg')

            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e

    def getShekhar(self)-> object:
        return {"apple": "apple", "banana": "banana"}