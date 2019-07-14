import simplejson
from flask import (make_response, Blueprint, current_app)
from ..controllers import campus as campus_controller
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import generic_handler, login_required, load_context


bp = Blueprint('campus', __name__, url_prefix='/campus')
bp.register_error_handler(ErroInterno, generic_handler)
bp.register_error_handler(UsoInvalido, generic_handler)


@bp.route('/', methods=('GET',))
@load_context
@login_required
def get_campus():
    """
    View function para recuperar os campi disponíveis.

    :return: 200 - uma lista de campi disponíveis.
             404 - erro na requisição.
             500 - erro interno.
    """
    try:
        resultado = campus_controller.recuperar_campus()

        response = make_response(resultado, 200)
        response.headers['Content-Type'] = 'application/json'

        return response
    except UsoInvalido as e:
        raise e
    except ErroInterno as e:
        raise e
    except Exception as e:
        raise ErroInterno(e, TipoErro.ERRO_INTERNO.name, payload="Erro ao recuperar campi.")
