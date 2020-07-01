import logging

from dynaconf import FlaskDynaconf, settings
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from .commons.logger import logger
from .errors import ErroInterno, TipoErro, UsoInvalido
from .models.db import db, ma

__author__ = "Igor Cavalcanti"
__email__ = "cavalcantigor at gmail dot com"
__version__ = "v0.1.0"


def setup_logger(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def get_tenant():
    if settings.ENABLE_MULTI_TENANT:
        db.choose_tenant(
            request.headers.get("Context", settings.DEFAULT_TENANT)
        )


def generic_handler(error):
    """
    Handler genérico de erros. Espera um objeto do tipo
    Exception que contenha uma funcao [to_dict] e um atributo
    [status_code] a fim de preparar a resposta do erro no
    formato JSON.

    :param error: objeto a ser tratado pelo handler.
    :return: um objeto JSON a ser enviado como resposta para o requisitante.
    """
    if isinstance(error, UsoInvalido):
        logger.info(error.payload)
    else:
        logger.error(error.payload, error.ex)

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def create_app():

    # cria e configura a aplicacao
    app = Flask(__name__, instance_relative_config=True)

    setup_logger(app)

    # modificando prefixo da url
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=settings.API_PREFIX)

    FlaskDynaconf().init_app(app)

    # registra as blueprints de resources
    from .resources.campus import bp as bp_campus
    from .resources.aluno import bp as bp_aluno
    from .resources.docs import bp as bp_docs

    app.register_blueprint(bp_campus)
    app.register_blueprint(bp_aluno)
    app.register_blueprint(bp_docs)

    db.init_app(app)
    ma.init_app(app)
    Migrate().init_app(app, db)
    CORS().init_app(app)

    app.before_request(logger.request)
    app.before_request(get_tenant)

    app.register_error_handler(ErroInterno, generic_handler)
    app.register_error_handler(UsoInvalido, generic_handler)

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
