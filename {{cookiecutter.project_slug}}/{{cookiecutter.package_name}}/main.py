import pathlib
import time
import sentry_sdk
from fastapi import FastAPI, Request
from starlette_exporter import PrometheusMiddleware, handle_metrics
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from {{cookiecutter.project_slug}}.api import {{cookiecutter.project_slug}}, info
from {{cookiecutter.project_slug}}.api.middlewares.errors import catch_exceptions_middleware
from {{cookiecutter.project_slug}}.exception import UnauthorizedAccess
from {{cookiecutter.project_slug}}.config import GCONFIG


if "url" in GCONFIG.sentry:
    sentry_sdk.init(  # pylint: disable=abstract-class-instantiated # noqa: E0110
        dsn=GCONFIG.sentry["url"],
        traces_sample_rate=1.0,
        environment=GCONFIG.sentry["environment"],
    )


app = FastAPI()


def _create_tmp_dir():
    pathlib.Path(GCONFIG.{{cookiecutter.project_slug}}["download_dir"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(GCONFIG.{{cookiecutter.project_slug}}["prometheus_dir"]).mkdir(parents=True, exist_ok=True)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

async def add_check_token(request: Request, call_next):
    if GCONFIG.{{cookiecutter.project_slug}}["token"] and (
        "token" not in request.headers
        or request.headers["token"] != GCONFIG.{{cookiecutter.project_slug}}["token"]
    ):
        raise UnauthorizedAccess("NoAuth")
    return await call_next(request)


_create_tmp_dir()
app.add_middleware(PrometheusMiddleware, app_name="{{cookiecutter.project_slug}}")
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(SentryAsgiMiddleware)
app.add_route("/metrics", handle_metrics)
app.middleware("http")(catch_exceptions_middleware)
### Uncomment to check a token before serving the API
# app.middleware("http")(add_check_token)
app.include_router(info.router)
app.include_router({{cookiecutter.project_slug}}.router)
