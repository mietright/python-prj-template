import pathlib
import time
from fastapi import FastAPI, Request
from ibanchecker.api import iban, info
from ibanchecker.api.middlewares.errors import catch_exceptions_middleware
from ibanchecker.config import GCONFIG

app = FastAPI()


def _create_dl_dir():
    pathlib.Path(GCONFIG.ibanchecker["download_dir"]).mkdir(parents=True, exist_ok=True)


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
app.include_router(iban.router)
