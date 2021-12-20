import json

from fastapi import FastAPI

from {{cookiecutter.package_name}}.api import {{cookiecutter.package_name}} as api


def _set_attrs(app, api):
    for attr in [
        "title",
        "description",
        "version",
        "terms_of_service",
        "license_info",
        "servers",
    ]:
        value = getattr(api, attr, None)
        if value is not None:
            setattr(app, attr, value)


def openapi():
    app = FastAPI()
    _set_attrs(app, api)
    app.include_router(api.router)
    print(json.dumps(app.openapi()))
