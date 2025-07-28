from typing import Any
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from app.constants import messages


class ResponseBuilder:
    def build_success_response(self, message: str= None, data: any = None):
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "status": "success",
                "message": message,
                "data": data,
            }
        )

    def build_created_response(self, message: str, data: any = None):
        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={
                "status": "success",
                "message": message,
                "data": data,
            }
        )

    def build_no_content_response(self):
        return JSONResponse(
            status_code=HTTP_204_NO_CONTENT,
            content=None
        )

    def build_bad_request_response(self, message: str, data: any = None):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "message": message,
                "data": data,
            }
        )

    def build_unauthorized_response(self, message: str = "Unauthorized"):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": message,
            }
        )

    def build_forbidden_response(self, message: str = "Forbidden"):
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={
                "status": "error",
                "message": message,
            }
        )

    def build_not_found_response(self, message: str = "Not found"):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "message": message,
            }
        )

    def build_conflict_response(self, message: str, data: any = None):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={
                "status": "error",
                "message": message,
                "data": data,
            }
        )

    def build_server_error_response(self, message: str = "Internal Server Error", data: Any = None) -> JSONResponse:
        """
        Builds a standardized 500 Internal Server Error response.

        Args:
            message (str): Error message to return.
            data (Any): Optional additional data (e.g., error details).

        Returns:
            JSONResponse: Formatted error response with HTTP 500 status.
        """
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": message,
                "data": data
            }
        )
