from typing import Dict, Optional

from fastapi import HTTPException, Response, status
from pydantic import BaseModel, Field, root_validator


NOTIFICATION_TYPE = ["success", "error", "warning"]

STANDARD_RESPONSES = {
    "201": {
        "description": "Requested resource created successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "Resource created",
                    "success": True,
                    "data": {},
                    "paginator": {},
                }
            }
        },
    },
    "204": {
        "description": "Requested resource deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "Resource deleted",
                    "success": True,
                    "data": {},
                    "paginator": {},
                }
            }
        },
    },
    "400": {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                    "message": "Bad request",
                    "success": False,
                    "data": {},
                    "paginator": {},
                }
            }
        },
    },
    "404": {
        "description": "Resource not found for your request.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Resource not found",
                    "success": False,
                    "data": {},
                    "paginator": {},
                }
            }
        },
    },
    "500": {
        "description": "Internal server Error occurred while working on API request",
        "content": {
            "application/json": {
                "example": {
                    "message": "Internal server error",
                    "success": False,
                    "data": {},
                    "paginator": {},
                }
            }
        },
    },
}


class StandardNotificationResponseModel(BaseModel):
    """
    Standard response model for all notification.
    Attributes:
    -----------
    header : str
        Header indicating Eaglai-hub Backend.
    message : str
        Should be message you want user to see.
    n_type : str
        error could be [success , error, warning].
    description : str
        Description of the message should be here.
    """

    header: str = "Eaglai-hub"
    message: str
    n_type: str = "error"
    description: str = "Default description"

    @root_validator
    def validate_fields(cls, values):
        if values["n_type"] not in NOTIFICATION_TYPE:
            raise ValueError(f"Invalid n_type provided: {values['n_type']}")
        return values


class StandardResponse(BaseModel):
    """
    Standard response model for all API endpoints.

    Attributes:
    -----------
    message : str
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    paginator : dict, optional
        Dictionary containing pagination information.
    # data : dict or list, optional
    #     Data returned by the API endpoint.
    """

    message: str = Field(..., example="Ok")
    success: Optional[bool] = Field(..., example=True)
    paginator: Optional[Dict] = {}
    # data: Optional[Union[Dict, List]] = Field(..., example={})


def response_ok(
    message="Ok",
    success=True,
    data={},
    paginator={},
):
    """
    Returns a 200 OK response.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    --------
    dict
        Standard response with HTTP status code 200.
    """
    response_data = {
        "message": message,
        "success": success,
        "data": data,
        "paginator": paginator,
    }
    return response_data


def response_created(
    message="Resource created",
    success=True,
    data={},
    paginator={},
):
    """
    Returns a 201 Created response.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    -------
    dict
        Standard response with HTTP status code 201.
    """

    response_data = {
        "message": message,
        "success": success,
        "data": data,
        "paginator": paginator,
    }
    return response_data


def response_no_content():
    """
    Returns a 204 No Content response.

    Returns:
    --------
        status_code (int): Status code 204

    NOTE: This methods should only be called for DELETE requests, It will not return anything
    """
    code = status.HTTP_204_NO_CONTENT
    return Response(status_code=code)

def response_conflict(message="Conflict",success=False):
    code = status.HTTP_409_CONFLICT
    data = {
        "message": message,
        "success": False,
    }
    raise HTTPException(status_code=code, detail=data)

def response_bad_request(
    message="Bad Request",
    success=False,
    data={},
    paginator={},
):
    """
    Returns a 400 Bad Request response.
    This method should only be called when the requested data is not enough to complete the request.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    --------
    HTTPException
        Exception with HTTP status code 400 and standard response data.
    """
    code = status.HTTP_400_BAD_REQUEST
    data = {
        "message": message,
        "success": success,
        "data": data,
        "paginator": paginator,
    }
    raise HTTPException(status_code=code, detail=data)


def response_too_many_active_sessions(
    message="Multiple Sessions are active",
):
    """
    Returns a 400 Bad Request response for too many active sessions.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    --------
    HTTPException
        Exception with HTTP status code 400 and standard response data.
    """
    code = status.HTTP_400_BAD_REQUEST
    data = {
        "message": message,
        "success": False,
    }
    raise HTTPException(status_code=code, detail=data)


def response_unauthenticate(
    message="Unauthenticate",
    success=False,
    data={},
    paginator={},
):
    """
    Returns a 401 Unauthenticate response.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    --------
    HTTPException
        Exception with HTTP status code 401 and standard response data.
    """
    code = status.HTTP_401_UNAUTHORIZED
    data = {
        "message": message,
        "success": success,
        "data": data,
        "paginator": paginator,
    }
    raise HTTPException(status_code=code, detail=data)


def response_not_found(
    message="Not Found",
    success=False,
    data={},
    paginator={},
):
    """
    Returns a 404 Not Found response.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    --------
    HTTPException
        Exception with HTTP status code 404 and standard response data.
    """
    code = status.HTTP_404_NOT_FOUND
    data = {
        "message": message,
        "success": success,
        "data": data,
        "paginator": paginator,
    }
    raise HTTPException(status_code=code, detail=data)


def response_sesion_not_available(message="Session not available"):
    """
    Returns a 404 Not found response for session not available.
    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.
    Returns:
    --------
    HTTPException
        Exception with HTTP status code 203 and standard response data.
    """
    code = status.HTTP_404_NOT_FOUND
    data = {
        "message": message,
        "success": False,
    }
    raise HTTPException(status_code=code, detail=data)


def response_internal_server_error(
    message="Internal server error",
    success=False,
    data={},
    paginator={},
):
    """
    Returns a 500 Internal Server Error response.

    Parameters:
    -----------
    message : str, optional
        Message indicating the result of the API call.
    success : bool, optional
        Boolean indicating whether the API call was successful.
    data : dict or list, optional
        Data returned by the API endpoint.
    paginator : dict, optional
        Dictionary containing pagination information.

    Returns:
    --------
    HTTPException
        Exception with HTTP status code 500 and standard response data.
    """
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data = {
        "message": message,
        "success": success,
        "data": data,
        "paginator": paginator,
    }
    raise HTTPException(status_code=code, detail=data)

