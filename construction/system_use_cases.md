~~Here are the system use cases for the openAI image generated management system:

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

These use cases cover all the operations that can be performed by the system. They provide a clear understanding of how the system interacts with the user and how it processes the user's requests.~~