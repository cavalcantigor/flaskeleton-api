from flask import Blueprint, render_template

from ..errors import ErroInterno, TipoErro

bp = Blueprint("docs", __name__, url_prefix="/apidocs")


@bp.route("/", methods=("GET",))
def apidocs():
    try:
        return render_template("/apidocs/index.html")
    except Exception as e:
        raise ErroInterno(
            TipoErro.ERRO_INTERNO.name,
            ex=e,
            payload="Erro ao renderizar documentação.",
        )
