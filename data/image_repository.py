from abc import ABC, abstractmethod
from data.__init__ import get_current_db_context
from core.models import ImageDetail

class IRepository(ABC):
    @abstractmethod
    def create(self, entity: ImageDetail) -> ImageDetail:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> ImageDetail:
        pass

    @abstractmethod
    def get_all(self) -> list[ImageDetail]:
        pass

class ImageRepository(IRepository):
    def create(self, image: ImageDetail) -> ImageDetail:
        print(f"i am saving in db {image.guid}")
        db = get_current_db_context()
        query = """
            INSERT INTO images (guid, filename, prompt)
            VALUES (%s, %s, %s)
            """
        values = (image.guid, image.filename, image.prompt)
        db.cursor.execute(query, values)
        db.connection.commit()
        # image.id = db.cursor.lastrowid
        return image

    def get_by_guid(self, guid: str) -> ImageDetail:
        db = get_current_db_context()
        query = "SELECT * FROM images WHERE guid = %s"
        values = (guid,)
        db.cursor.execute(query, values)
        result = db.cursor.fetchone()
        if result:
            return ImageDetail(**result)

    def get_all(self) -> list[ImageDetail]:
        db = get_current_db_context()
        query = "SELECT * FROM images"
        db.cursor.execute(query)
        results = db.cursor.fetchall()
        return [ImageDetail(**result) for result in results]
