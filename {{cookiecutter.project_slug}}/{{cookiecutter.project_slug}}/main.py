import pathlib
import time
from fastapi import FastAPI, Request
from {{cookiecutter.project_slug}}.api import {{cookiecutter.project_slug}}, info
from {{cookiecutter.project_slug}}.api.middlewares.errors import catch_exceptions_middleware
from {{cookiecutter.project_slug}}.config import GCONFIG

app = FastAPI()


def _create_dl_dir():
    pathlib.Path(GCONFIG.{{cookiecutter.project_slug}}["download_dir"]).mkdir(parents=True, exist_ok=True)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


_create_dl_dir()
app.middleware("http")(catch_exceptions_middleware)
app.include_router(info.router)
app.include_router({{cookiecutter.project_slug}}.router)
