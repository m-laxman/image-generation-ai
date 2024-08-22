It seems like we would need the following use cases to make our API useful:
Remember that guids are used to identify images.

* Create an image. When we create an image, we must specify a prompt. The API will generate an image (and image detail) from the prompt and return an `ImageDetail` model object that includes the prompt, filename, and guid.

* Get image details for an image with the provided guid. The API will return an `ImageDetail` model object that includes the prompt, filename, and guid.

* Get image details for all images. The API will return a list of `ImageDetail` model objects. Each `ImageDetail` object includes the prompt, filename, and guid of an image.

* Retrieve an image file using the provided guid. The API will return the image bytes in the body of the HTTP response.

All these operations can also be performed on private images after authentication has occurred.
We will use HTTP basic authentication against a known set of users.
