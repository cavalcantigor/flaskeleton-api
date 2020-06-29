from flask import request
from functools import wraps
from ..errors import TipoErro, UsoInvalido


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # implementar aqui uma funcao de autorizacao
        # abaixo um exemplo basico com o token estatico `123`
        if "Authorization" in request.headers:
            if request.headers["Authorization"] != "123":
                raise UsoInvalido(
                    TipoErro.NAO_AUTORIZADO.name,
                    status_code=401,
                    payload="Token inválido.",
                )
        else:
            raise UsoInvalido(
                TipoErro.NAO_AUTORIZADO.name,
                status_code=401,
                payload="Cabeçalho de autorização não " "encontrado.",
            )
        return f(*args, **kwargs)

    return decorated_function
