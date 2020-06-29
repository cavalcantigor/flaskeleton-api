from flask import make_response, Blueprint, request, jsonify
from ..controllers.aluno import AlunoController
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import login_required


bp = Blueprint("aluno", __name__, url_prefix="/aluno")


@bp.route("/", methods=["POST"])
@login_required
def create():
    try:
        aluno_controller = AlunoController()
        if request.is_json:
            aluno = aluno_controller.criar_aluno(request.json)

            resposta = make_response(aluno, 201)
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
            TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao criar aluno."
        )


@bp.route("/<int:codigo>", methods=["GET"])
@bp.route("/", methods=["GET"])
def retrieve(codigo: int = None):
    try:
        aluno_controller = AlunoController(codigo)

        resposta = make_response(
            jsonify(aluno_controller.recuperar_aluno()), 200
        )
        resposta.headers["Content-Type"] = "application/json"

        return resposta
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name,
            ex=e,
            payload="Erro ao recuperar aluno.",
        )


@bp.route("/<int:codigo>", methods=["PUT"])
@login_required
def update(codigo: int):
    try:
        aluno_controller = AlunoController(codigo)
        if request.is_json:
            request.json["codigo"] = codigo
            aluno = aluno_controller.atualizar_aluno(request.json)

            resposta = make_response(aluno, 200)
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
            payload="Erro ao atualizar aluno.",
        )


@bp.route("/<int:codigo>", methods=["DELETE"])
@login_required
def delete(codigo: int):
    try:
        aluno_controller = AlunoController(codigo)
        aluno_controller.deletar_aluno()

        return "", 204
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao deletar aluno."
        )
