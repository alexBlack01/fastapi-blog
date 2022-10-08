import logging
import time

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import Response

from adapters import postgres
from adapters.implementations.posts import PostsLocalPostgres
from applications.rest import v1
from domain.posts.repositories.posts import PostAppRepository
from shared import applications, container, exceptions

app = FastAPI(
    default_response_class=applications.ORJSONResponse,
    dependencies=[Depends(applications.request_logger)],
    openapi_url='/docs/openapi.json',
)
app.include_router(v1.router)


@app.middleware('http')
async def request_execution_time(request: Request, call_next):
    start = time.perf_counter()
    logger = container.resolve(logging.Logger)
    response: Response = await call_next(request)

    logger.info('api_request_done', extra={
        'api_request': {
            'execution_time_ms': round((time.perf_counter() - start) * 1000),
        },
    })

    return response


@app.exception_handler(exceptions.AppException)
async def uvicorn_api_exception_handler(
    request: Request,
    exc: exceptions.AppException,
):
    exception = exc.dict()

    return applications.ORJSONResponse(
        status_code=exc.status_code,
        content=exception,
    )


@app.exception_handler(Exception)
async def unicorn_base_exception_handler(request: Request, exc: Exception):
    error = exceptions.AppException(debug=str(exc))

    return applications.ORJSONResponse(
        status_code=error.status_code,
        content=error.dict(),
    )


@app.on_event('startup')
async def on_startup():
    await postgres.init_postgres()
    await postgres.stop_postgres()
    await applications.init_logger()
    container.register(logging.Logger, instance=logging.getLogger('app'))
    container.register(PostAppRepository, PostsLocalPostgres)


@app.on_event('shutdown')
async def on_shutdown():
    await postgres.stop_postgres()


if __name__ == '__main__':
    uvicorn.run(
        '__main__:app',
        host='0.0.0.0',  # noqa: S104
        port=8000,  # noqa: WPS432
        reload=True,
    )

