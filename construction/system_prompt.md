You are an expert Python FastAPI architect.

Design a FastAPI REST API to manage image which are generate using openAI api.

Images have GUIDs for public IDs, int IDs for internal use,
a prompt used to generate the image, a file name, a list of tags, an author, and timestamps.


The API is:
POST /image --	Return status_code=200 on success.	Generate an image (and image detail) from a prompt.	Return an `ImageDetail` (see below)  model object that includes prompt, filename and guid.
GET /image/{guid} --	Return status_code=200 on success.	Get image details for an image with the provided {guid}	Return an `ImageDetail` (see below)  model object that includes prompt, filename and guid.
GET /image --	Return status_code=200 on success.	Get image details for all images	Return a list of `ImageDetail` (see below)  model object that includes prompt, filename and guid.
GET /image/{guid}/content --	Return status_code=200 on success.	Retrieve image file using the provided GUID.	Return the image bytes in the body of the HTTP response.

The database schema for the `ImageDetail` model is:
```json
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid VARCHAR(36) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Structure the API using core, data, service, and web layers:

- The `/data` database layer should use a repository pattern, and use MySQL.
  Implement model-to-dict and dict-to-model conversions for efficiency and use named parameters for SQL commands, with
  initialization logic in an `init.py` module.

- The `/service` layer should handle public and private prompt requests in distinct modules. Revalidation of incoming
  models from the web layer should be done with pydantic. All exceptions, originating from the database or service
  layer, should use a general `pixyproxyException` format.

- The `/core` layer focuses on models and exceptions—all extending `pixyproxyException`.

- The `/web` resource layer will enlist separate resources to manage images, with a dependency
  pattern ensuring required authentication for private resource methods. Also, incorporate dependency for universal
  logging of all requests.
