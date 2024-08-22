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