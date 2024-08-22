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