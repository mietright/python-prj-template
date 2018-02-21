from flask import Flask, request
from flask_cors import CORS
from {{cookiecutter.project_slug}}.config import GCONFIG
from {{cookiecutter.project_slug}}.exception import {{cookiecutter.baseclass}}Exception
from {{cookiecutter.project_slug}}.api.handlers.errors import render_error
from {{cookiecutter.project_slug}}.api.handlers.request_logging import before_request_log, after_request_log
from {{cookiecutter.project_slug}}.api.flaskapp import FlaskApp


def getvalues():
    jsonbody = request.get_json(force=True, silent=True)
    values = request.values.to_dict()
    if jsonbody:
        values.update(jsonbody)
    return values


class {{cookiecutter.baseclass }}App(FlaskApp):
    from {{cookiecutter.project_slug}}.api.info import info_app

    blueprints = [(info_app, "")]
    before_request_funcs = [before_request_log]
    after_request_funcs = [after_request_log]
    error_handler_funcs = [({{cookiecutter.baseclass}}Exception, render_error)]


def create_app():
    app = Flask(__name__)
    CORS(app)
    ffapp = {{cookiecutter.baseclass }}App(app)
    # app.logger.addHandler(logging.StreamHandler(sys.stdout))
    # app.logger.setLevel(logging.INFO)
    if GCONFIG.{{ cookiecutter.project_slug }}['env'] != 'production':
        ffapp.app.config.from_object(
            '{{cookiecutter.project_slug}}.api.config.DevelopmentConfig')
    else:
        ffapp.app.config.from_object('{{cookiecutter.project_slug}}.api.config.ProductionConfig')

    ffapp.app.logger.info("Start service")
    return ffapp


if __name__ == "__main__":
    application = create_app().app
    application.run(host='0.0.0.0')
