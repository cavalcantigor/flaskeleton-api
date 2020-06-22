from ..errors import ErroInterno, TipoErro, UsoInvalido
from ..dao.campus import CampusDAO
from ..models.campus import Campus, CampusSchema
from ..logger import logger
from marshmallow import ValidationError


class CampusController:

    def __init__(self, codigo: int = None):
        self.__campus_schema = CampusSchema()
        self.__campus = Campus(codigo=codigo)
        self.__campus_dao = CampusDAO(self.__campus)

    def recuperar_campus(self) -> list or Campus:
        try:
            resultado = self.__campus_dao.get()
            if resultado is not None:
                logger.info("campus recuperado com sucesso")
                if isinstance(resultado, list):
                    return self.__campus_schema.dump(resultado, many=True)
                else:
                    return self.__campus_schema.dump(resultado)
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Campus não foi encontrado.",
                    status_code=404,
                )
        except (ErroInterno, UsoInvalido) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Erro ao recuperar campi disponíveis.",
            )

    def criar_campus(self, campus: dict = None) -> Campus:
        try:
            if self.__campus.codigo:
                raise UsoInvalido(
                    TipoErro.ALUNO_DUPLICADO.name, ex="Campus já existe."
                )
            else:
                if campus:
                    self.__campus = CampusSchema().load(campus, session=self.__campus_dao.session)
                    self.__campus_dao = CampusDAO(self.__campus)
                    self.__campus_dao.insert()
                    logger.info(
                        "campus {} criado com sucesso".format(
                            str(self.__campus)
                        )
                    )
                    return self.__campus_schema.dump(self.__campus)
                else:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name,
                        ex="Objeto Campus a ser inserido está nulo ou "
                        "vazio.",
                    )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except ValidationError as e:
            raise UsoInvalido(
                TipoErro.ERRO_VALIDACAO.name, payload=str(e.messages)
            )
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao criar Campus.",
            )

    def atualizar_campus(self, campus: dict = None) -> Campus:
        try:
            self.__campus = self.__campus_dao.get()
            self.__campus_dao = CampusDAO(self.__campus)
            if self.__campus:
                if campus:
                    self.__campus = CampusSchema().load(campus)
                    self.__campus_dao = CampusDAO(self.__campus)
                    self.__campus_dao.update()
                    logger.info("campus atualizado com sucesso")
                    return CampusSchema().jsonify(self.__campus)
                else:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name,
                        payload="Objeto Campus a ser atualizado está nulo "
                        "ou vazio.",
                    )
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Campus não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except ValidationError as e:
            raise UsoInvalido(
                TipoErro.ERRO_VALIDACAO.name, payload=str(e.messages)
            )
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao atualizar Campus.",
            )

    def deletar_campus(self) -> bool:
        try:
            self.__campus = self.__campus_dao.get()
            self.__campus_dao = CampusDAO(self.__campus)
            if self.__campus:
                if self.__campus_dao.delete():
                    logger.info(
                        "campus {} deletado com sucesso".format(self.__campus.codigo)
                    )
                    return True
                else:
                    return False
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Aluno não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao deletar Campus.",
            )
