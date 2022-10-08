import logging
from json.decoder import JSONDecodeError
from typing import Any

import orjson
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.requests import Request

from shared import container
from shared.utils import orjson_dumps


class BaseAppModel(BaseModel):
    """Base application model for value-objects and entities."""

    pass

    class Config(object):
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ORJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:  # noqa: WPS110
        return orjson.dumps(content, option=orjson.OPT_NAIVE_UTC | orjson.OPT_NON_STR_KEYS)


async def request_logger(request: Request):
    logger = container.resolve(logging.Logger)
    headers = {key: request.headers.getlist(key) for key in request.headers.keys()}
    query_params = {key: query_value for key, query_value in request.query_params.items()}
    path_params = {key: path_value for key, path_value in request.path_params.items()}

    body = ''

    if 'application/json' in request.headers.getlist('Content-Type'):
        try:
            body = orjson.dumps(await request.json(), option=orjson.OPT_INDENT_2).decode()
        except JSONDecodeError:
            body = (await request.body()).decode()

    logger.info('api_request', extra={
        'request': {
            'headers': orjson.dumps(headers, option=orjson.OPT_INDENT_2).decode(),
            'body': body,
            'query_params': orjson.dumps(query_params).decode(),
            'path_params': orjson.dumps(path_params).decode(),
            'url': request.url.path,
            'method': request.method,
            'base_url': request.base_url.hostname,
        },
    })


async def init_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)
