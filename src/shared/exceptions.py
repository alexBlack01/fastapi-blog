from typing import Any, Dict, List, Mapping, Optional, Type

from fastapi import status


class AppException(Exception):
    """Base application exception with HTTP metadata."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
            self,
            message: Optional[str] = None,
            payload: Optional[Mapping] = None,
            debug: Any = None,
    ):
        self.message = message or 'Internal server error'
        self.payload = payload
        self.debug = debug

    @classmethod
    def exception_code(cls):
        return cls.__name__

    def dict(self) -> Mapping:
        return {
            'code': self.exception_code(),
            'message': self.message,
            'payload': self.payload,
            'debug': self.debug,
        }


def exception_schema(exceptions: List[Type[AppException]]):
    """Fastapi exception schema to document custom responses.

    Use result of this function to as :responses param of FastApi endpoint decorator

    :param exceptions:
        List of exception types to show in docs
    """
    responses: Dict[int, Dict] = {}

    schema = {
        'type': 'object',
        'properties': {
            'code': {
                'type': 'string',
                'title': 'Exception code',
            },
            'message': {
                'type': 'string',
                'title': 'Exception message',
            },
            'payload': {
                'type': 'object',
                'title': 'Exception body',
            },
            'debug': {
                'type': 'string',
                'title': 'Debug info',
            },
        },
    }

    for exc in exceptions:
        code = exc.exception_code()

        if exc.status_code not in responses:
            responses[exc.status_code] = {}

        responses[exc.status_code][code] = {
            'value': {
                'code': code,
                'message': exc.message,
            },
        }

    return {
        status_code: {
            'content': {
                'application/json': {
                    'schema': schema,
                    'examples': examples,
                },
            },
        }
        for status_code, examples in responses.items()
    }
