from typing import Any, Optional, Dict

from fastapi import status, HTTPException


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        errors: Optional[dict] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.errors = errors
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundError(CustomHTTPException):
    def __init__(self, detail: Any = "Object not found", errors: Optional[dict] = None):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, errors)


class ValidationError(CustomHTTPException):
    def __init__(self, detail: Any = "Validation error", errors: Optional[dict] = None):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, errors)


class AlreadyExistsError(CustomHTTPException):
    def __init__(self, detail: Any = "Object already exists", errors: Optional[dict] = None):
        super().__init__(status.HTTP_409_CONFLICT, detail, errors)


class RelatedObjectError(CustomHTTPException):
    def __init__(
        self, detail: Any = "Object is related to other objects", errors: Optional[dict] = None
    ):
        super().__init__(status.HTTP_409_CONFLICT, detail, errors)
