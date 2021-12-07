import json
import logging

import click
from fastapi import FastAPI

from {{cookiecutter.package_name}}.api import {{cookiecutter.package_name}} as api


def openapi():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    app = FastAPI()
    app.include_router(api.router)
    print(json.dumps(app.openapi()))
