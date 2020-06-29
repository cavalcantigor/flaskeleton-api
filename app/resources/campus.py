from flask import make_response, Blueprint, request, jsonify
from ..controllers.campus import CampusController
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import login_required


bp = Blueprint("campus", __name__, url_prefix="/campus")


@bp.route("/", methods=["POST"])
@login_required
def create():
    try:
        campus_controller = CampusController()
        if request.is_json:
            campus = campus_controller.criar_campus(request.json)

            resposta = make_response(campus, 201)
            resposta.headers["Content-Type"] = "application/json"

            return resposta
        else:
            raise UsoInvalido(
                TipoErro.ERRO_VALIDACAO.name,
                payload="Payload não está no formato JSON.",
            )
    except (ErroInterno, UsoInvalido) as e:
        raise e
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao criar campus."
        )


@bp.route("/<int:codigo>", methods=["GET"])
@bp.route("/", methods=["GET"])
def retrieve(codigo: int = None):
    try:
        campus_controller = CampusController(codigo=codigo)

        resposta = make_response(
            jsonify(campus_controller.recuperar_campus()), 200
        )
        resposta.headers["Content-Type"] = "application/json"

        return resposta
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name,
            ex=e,
            payload="Erro ao recuperar campus.",
        )


@bp.route("/<int:codigo>", methods=["PUT"])
@login_required
def update(codigo: int):
    try:
        campus_controller = CampusController(codigo=codigo)
        if request.is_json:
            request.json["codigo"] = codigo
            resposta = make_response(
                campus_controller.atualizar_campus(request.json), 200
            )
            resposta.headers["Content-Type"] = "application/json"

            return resposta
        else:
            raise UsoInvalido(
                TipoErro.ERRO_VALIDACAO.name,
                payload="Payload não está no formato JSON.",
            )
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name,
            ex=e,
            payload="Erro ao atualizar campus.",
        )


@bp.route("/<int:codigo>", methods=["DELETE"])
@login_required
def delete(codigo: int):
    try:
        campus_controller = CampusController(codigo=codigo)
        campus_controller.deletar_campus()

        return "", 204
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao deletar campus."
        )
