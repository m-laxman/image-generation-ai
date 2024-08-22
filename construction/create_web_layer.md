Lets build the web layer for the following system and service layer.
Let's use FastAPI to do this.

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
    
These use cases cover all the operations that can be performed by the system. They provide a clear understanding of how the system interacts with the user and how it processes the user's requests.
```

Here is the image service interface to use:
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
# service/image_service.py
import traceback
from typing import List
from core.models import ImageDetail, ImageDetailCreate
from core.exceptions import RecordNotFoundError, ImageException
from service.image_service_interface import ImageServiceInterface
from data import get_current_db_context, DatabaseContext


class ImageService(ImageServiceInterface):
    def create_image(self, image_create: ImageDetailCreate) -> ImageDetail:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                # TODO: Implement the logic to create an image
                db.commit_transaction()
            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e

    def get_image_by_guid(self, guid: str) -> ImageDetail:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                # TODO: Implement the logic to get an image by guid
                db.commit_transaction()
            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e

    def get_all_images(self) -> List[ImageDetail]:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                # TODO: Implement the logic to get all images
                db.commit_transaction()
            except ImageException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageException("An unexpected error occurred while processing your request.") from e
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

Here are the core exceptions to use:
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
        

# 2. Service Layer Exceptions

class DataValidationError(PromptException):
    def __init__(self, message="Provided data is invalid."):
        super().__init__(message)


class UnauthorizedError(PromptException):
    def __init__(self, message="Unauthorized access."):
        super().__init__(message)


class OperationNotAllowedError(PromptException):
    def __init__(self, message="This operation is not allowed."):
        super().__init__(message)


# 3. Web Layer Exceptions

class BadRequestError(PromptException):
    def __init__(self, message="Bad request data."):
        super().__init__(message)


class EndpointNotFoundError(PromptException):
    def __init__(self, message="Endpoint not found."):
        super().__init__(message)


class AuthenticationError(ImageException):
    def __init__(self, message="Authentication failed."):
        super().__init__(message)

EXCEPTION_STATUS_CODES = {
    DataValidationError: 400,       # Bad Request
    ConstraintViolationError: 409,  # Conflict
    PromptException: 500,           # Internal Server Error (Generic fallback)
    DBConnectionError: 500,         # Internal Server Error (Generic fallback)
    RecordNotFoundError: 404,       # Not Found
    UnauthorizedError: 401,         # Unauthorized
    OperationNotAllowedError: 403,  # Forbidden
    BadRequestError: 400,           # Bad Request
    EndpointNotFoundError: 404,     # Not Found
    AuthenticationError: 401,       # Unauthorized
}

```

The web layer is responsible for validation, central exception handling with a single exception handler,
and logging of each request (assigning a request id, logging the start and end result of each request per above).

Let's create a FastAPI application with a router for public prompts and a router for private prompts.
The public router should support read-only access to prompts before login.
The private router should support read-write access to prompts after login.

Let's use HTTP basic authentication for the private router, and implement a service layer repository and database level repository for user validation.
Let's write a global dependency so all endpoints are logged using the required format.

Let's generate a file at a time and pause to think upfront about how things will all fit together.

Then let's generate an API description with enough detail to write test cases for the web layer.
