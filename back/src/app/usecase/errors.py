class NotFoundError(Exception):
    """Exception raised when a resource is not found. 404 error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidInputError(Exception):
    """Exception raised when the input is invalid. 400 error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UnauthorizedError(Exception):
    """Exception raised when the user is not authorized to perform an action. 401 error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ForbiddenError(Exception):
    """Exception raised when the user does not have permission to perform an action. 403 error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InternalServerError(Exception):
    """Exception raised when an internal server error occurs. 500 error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RaffleProcessingError(InternalServerError):
    """Exception raised when raffle processing was not successful"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
