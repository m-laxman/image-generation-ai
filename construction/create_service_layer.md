Lets build the service layer for the following system and database schema.
Let's use the repository pattern with interfaces, models, and exceptions.

The system description is as follows:
```
The system is a FastAPI REST API designed to manage images generated using the OpenAI API. Each image is identified by a GUID for public use and an integer ID for internal use. The images also have a prompt used for their generation, a filename, a list of tags, an author, and timestamps.

The API consists of four endpoints:

1. `POST /image` - This endpoint is responsible for generating an image and its details from a given prompt. Upon successful operation, it returns an `ImageDetail` model object that includes the prompt, filename, and GUID of the image.

2. `GET /image/{guid}` - This endpoint retrieves the details of an image using the provided GUID. It returns an `ImageDetail` model object that includes the prompt, filename, and GUID of the image.

3. `GET /image` - This endpoint retrieves the details of all images and returns a list of `ImageDetail` model objects. Each `ImageDetail` object includes the prompt, filename, and GUID of an image.

4. `GET /image/{guid}/content` - This endpoint retrieves the image file using the provided GUID and returns the image bytes in the body of the HTTP response.

The `ImageDetail` model is stored in a MySQL database. The schema for this model includes fields for id, guid, filename, prompt, and timestamps.

The API is structured into four layers:

1. `/data` - This is the database layer that uses a repository pattern. It uses MySQL for data storage. This layer includes model-to-dict and dict-to-model conversions for efficiency and uses named parameters for SQL commands. The initialization logic for this layer is contained in an `init.py` module.

2. `/service` - This layer handles public and private prompt requests in distinct modules. It revalidates incoming models from the web layer using pydantic. All exceptions, whether they originate from the database or service layer, use a general `pixyproxyException` format.

3. `/core` - This layer focuses on models and exceptions. All exceptions in this layer extend the `pixyproxyException`.

4. `/web` - This is the resource layer that manages images. It uses a dependency pattern to ensure required authentication for private resource methods. It also incorporates a dependency for universal logging of all requests.

The system uses environment variables to configure the database connection. SQL scripts are used to create the database, user, and table. The project is structured using markdown files and the developer is working with Python and pip.
```

Let's make sure to cover the following use cases for our system:
```
Here are the system use cases for the openAI image generated management system:

1. **Create an Image**
    - **Actor**: User
    - **Description**: The user sends a POST request to `/image` with a prompt in the request body. The system generates an image and its details from the prompt and stores it in the database. The system then returns an `ImageDetail` model object that includes the prompt, filename, and guid of the image.

2. **Get Image Details by GUID**
    - **Actor**: User
    - **Description**: The user sends a GET request to `/image/{guid}`. The system retrieves the details of the image with the provided guid from the database and returns an `ImageDetail` model object that includes the prompt, filename, and guid of the image.

3. **Get Details of All Images**
    - **Actor**: User
    - **Description**: The user sends a GET request to `/image`. The system retrieves the details of all images from the database and returns a list of `ImageDetail` model objects. Each `ImageDetail` object includes the prompt, filename, and guid of an image.

4. **Retrieve Image File by GUID**
    - **Actor**: User
    - **Description**: The user sends a GET request to `/image/{guid}/content`. The system retrieves the image file with the provided guid from the database and returns the image bytes in the body of the HTTP response.

5. **Perform Operations on Private Images**
    - **Actor**: Authenticated User
    - **Description**: The user sends a request to any of the above endpoints with HTTP basic authentication. After successful authentication, the system performs the requested operation on the private images.

These use cases cover all the operations that can be performed by the system. They provide a clear understanding of how the system interacts with the user and how it processes the user's requests.
```

Here are the database repository interfaces to use:
```
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
```

Here are the core model objects to use:
```
from pydantic import BaseModel

class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str
```

Here are the exceptions to use:
```
class ImageException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DBConnectionError(ImageException):
    def __init__(self, message="Failed to connect to the database."):
        super().__init__(message)

class RecordNotFoundError(ImageException):
    def __init__(self, message="The requested record was not found."):
        super().__init__(message)

class ConstraintViolationError(ImageException):
    def __init__(self, message="A database constraint was violated."):
        super().__init__(message)
```

The service layer is responsible for transaction management and business logic and validation.
Create the service layer interface, then implement it.

Assume we have the following DatabaseContext class:
```
import mysql
from mysql.connector import pooling
from dotenv import load_dotenv
import os
import threading

load_dotenv()


# Database Configuration
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True,
}


# Create a thread-local storage
local_storage = threading.local()

# Create a connection pool
# db_pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=10, **config)


class DatabaseContext:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    @property
    def cursor(self):
        return self._cursor

    # Exposing transactional methods for use in service layer
    def begin_transaction(self):
        self.connection.start_transaction()

    def commit_transaction(self):
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()

    @cursor.setter
    def cursor(self, value):
        self._cursor = value


# Provide a global function to fetch the current context
def set_db_context():
    local_storage.db_context = DatabaseContext()

def get_current_db_context():
    local_storage.db_context = DatabaseContext()
    return getattr(local_storage, "db_context", None)


```

Let's generate:
* a list of files needed to cleanly implement the service interface and implementation
* complete code for the service layer
* implement Pydantic object violations for all public function signatures and return appropriate core exceptions
* each major service method should start and manage a transaction using the DatabaseContext class
* specify types and salient docstrings for all public function signatures
- Don't forget to separate initialisation code into service/init.py
- Let's assume use of python-dotenv to read in configuration items
- Include a sample .env file with any configuration items needed

Make a XServiceInterface class and a XService class for each of the following:
ImageService

The way we intend to use DatabaseContext is as follows:
 with DatabaseContext() as db:
            try:
                db.begin_transaction()
                # do some work
                db.commit_transaction()
                # return result
            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise PromptException("An unexpected error occurred while processing your request.") from e

```