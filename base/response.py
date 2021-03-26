from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response


def json_api_response(code, data, message):
    data = {
        "code": code,
        "data": data,
        "message": message
    }
    return Response(data, status=HTTP_200_OK)


def json_ok_response(data="success"):
    return json_api_response(code=0, data=data, message=None)


def json_error_response(message):
    return json_api_response(code=-1, data=None, message=message)
