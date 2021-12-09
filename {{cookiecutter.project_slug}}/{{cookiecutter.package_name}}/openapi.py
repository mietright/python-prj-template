import json

from fastapi import FastAPI

from {{cookiecutter.package_name}}.api import {{cookiecutter.package_name}} as api


def openapi():
    app = FastAPI()
    app.include_router(api.router)
    print(json.dumps(app.openapi()))
