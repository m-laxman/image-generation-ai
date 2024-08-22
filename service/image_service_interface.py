# service/image_service_interface.py
from abc import ABC, abstractmethod
from typing import List
from core.models import ImageDetail, ImageDetailCreate

class ImageServiceInterface(ABC):
    @abstractmethod
    def create_image(self, image_create: ImageDetailCreate) -> ImageDetail:
        pass

    @abstractmethod
    def get_image_by_guid(self, guid: str) -> ImageDetail:
        pass

    @abstractmethod
    def get_all_images(self) -> List[ImageDetail]:
        pass

    @abstractmethod
    def get_image_content(self, guid: str) -> ImageDetail:
        pass

    @abstractmethod
    def getShekhar(self) -> object:
        pass