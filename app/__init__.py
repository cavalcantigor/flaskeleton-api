import logging
from dynaconf import settings, FlaskDynaconf
from flask import Flask, request
from flask_cors import CORS
from .models.db import db, ma
from flask_migrate import Migrate
from .logger import logger
import os


__author__ = "Igor Cavalcanti"
__email__ = "cavalcantigor at gmail dot com"
__version__ = "v0.1.0"


def setup_logger(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def get_tenant():
    if settings.ENABLE_MULTI_TENANT:
        db.choose_tenant(request.headers.get("Context", settings.DEFAULT_TENANT))


def create_app():

    # cria e configura a aplicacao
    app = Flask(__name__, instance_relative_config=True)

    setup_logger(app)

    # modificando prefixo da url
    app.wsgi_app = PrefixMiddleware(
        app.wsgi_app, prefix=settings.API_PREFIX
    )

    FlaskDynaconf(app)

    # registra as blueprints de resources
    from .resources.campus import bp as bp_campus
    from .resources.aluno import bp as bp_aluno
    from .resources.docs import bp as bp_docs

    app.register_blueprint(bp_campus)
    app.register_blueprint(bp_aluno)
    app.register_blueprint(bp_docs)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841
    CORS(app)

    app.before_request(logger.request)
    app.before_request(get_tenant)

    return app


class PrefixMiddleware(object):
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response("404", [("Content-Type", "text/plain")])
            return [
                "Esta URL nao pertence a aplicacao. "
                "Por favor, insira o prefixo '{}'.".format(
                    self.prefix
                ).encode()
            ]
