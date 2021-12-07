import pathlib
from pathlib import Path
import time
import logging
import importlib.util

import aiohttp
import click
from fastapi import FastAPI, Request
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import uvicorn

from {{cookiecutter.package_name}}.api import {{cookiecutter.package_name}} as api
from {{cookiecutter.package_name}}.api import info
from {{cookiecutter.package_name}}.api.middlewares.errors import catch_exceptions_middleware
from {{cookiecutter.package_name}}.exception import UnauthorizedAccess
from {{cookiecutter.package_name}}.config import GCONFIG
from {{cookiecutter.package_name}}.openapi import openapi


if "url" in GCONFIG.sentry:
    sentry_sdk.init(  # pylint: disable=abstract-class-instantiated # noqa: E0110
        dsn=GCONFIG.sentry["url"],
        traces_sample_rate=1.0,
        environment=GCONFIG.sentry["environment"],
    )


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def add_check_token(request: Request, call_next):
    if GCONFIG.{{cookiecutter.package_name}}["token"] and (
        "token" not in request.headers
        or request.headers["token"] != GCONFIG.{{cookiecutter.package_name}}["token"]
    ):
        raise UnauthorizedAccess("NoAuth")
    return await call_next(request)


def _create_tmp_dir():
    pathlib.Path(GCONFIG.{{cookiecutter.package_name}}["download_dir"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(GCONFIG.{{cookiecutter.package_name}}["prometheus_dir"]).mkdir(parents=True, exist_ok=True)


_create_tmp_dir()
app.add_middleware(PrometheusMiddleware, app_name="{{cookiecutter.package_name}}")
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(SentryAsgiMiddleware)
app.add_route("/metrics", handle_metrics)
app.middleware("http")(catch_exceptions_middleware)
app.include_router(info.router)
app.include_router(api.router)
### Uncomment to check a token before serving the API
# app.middleware("http")(add_check_token)

@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--host", default="0.0.0.0", type=str, show_default=True)
@click.option("--port", default=8000, type=int, show_default=True)
def cli(ctx, host, port):
    if ctx.invoked_subcommand is None:
        log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        logger = logging.getLogger(__name__)

        logger.info(f"Using host {host}")
        logger.info(f"Using port {port}")
        uvicorn.run(app, host=host, port=port, log_level="debug")


cli.command("openapi")(openapi)

if __name__ == "__main__":
    main()
