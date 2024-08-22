Lets build the data layer for the following system and database schema.
Let's use DB-API to do this with a MYSQL backend.
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

Here is the database schema to use:
```
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `images` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `guid` VARCHAR(255) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `prompt` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `images_U1` UNIQUE (`guid`),
  INDEX `images_I1` (`filename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
Let's generate:
* a list of files needed to cleanly implement the provided Mysql version of the database
* complete code for the data layer using a repository pattern with interfaces, models, and exceptions

- Don't forget to separate initialisation code into data/init.py
- Let's assume use of python-dotenv to read in configuration items 
- Include a sample .env file with any configuration items needed
  - specify types and salient docstrings for all public function signatures
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
