from marshmallow import ValidationError

from ..commons.logger import logger
from ..dao.campus import CampusDAO
from ..errors import ErroInterno, TipoErro, UsoInvalido
from ..models.campus import Campus, CampusSchema


class CampusController:
    def __init__(self, codigo: int = None):
        self.__campus_schema = CampusSchema()
        self.__campus = Campus(codigo=codigo)
        self.__campus_dao = CampusDAO(self.__campus)

    def recuperar_campus(self) -> list or Campus:
        try:
            if self.__campus.codigo:
                self.__campus = self.__campus_dao.get()
                if self.__campus:
                    logger.info(
                        "campus {} recuperado(s) com sucesso".format(
                            self.__campus.codigo
                        )
                    )
                    return self.__campus_schema.dump(self.__campus)
                else:
                    raise UsoInvalido(
                        TipoErro.NAO_ENCONTRADO.name,
                        payload="Campus não foi encontrado.",
                        status_code=404,
                    )
            else:
                return self.__campus_schema.dump(
                    self.__campus_dao.get_all(), many=True
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao recuperar campus(s).",
            )

    def criar_campus(self, campus: dict = None) -> Campus:
        try:
            self.__campus = self.__campus_schema.load(
                campus, instance=self.__campus
            )
            self.__campus_dao = CampusDAO(self.__campus)
            self.__campus_dao.insert()
            logger.info(
                "campus {} criado com sucesso".format(str(self.__campus))
            )
            return self.__campus_schema.dump(self.__campus)
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
                payload="Ocorreu um erro ao criar campus.",
            )

    def atualizar_campus(self, dados_campus: dict = None) -> Campus:
        try:
            self.__campus = self.__campus_dao.get()
            if self.__campus:
                erros = self.__campus_schema.validate(dados_campus)
                if erros:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name, payload=str(erros)
                    )
                self.__campus_schema.update(self.__campus, dados_campus)
                self.__campus = self.__campus_dao.update()
                logger.info(
                    "campus {} atualizado com sucesso".format(
                        self.__campus.codigo
                    )
                )
                return self.__campus_schema.dump(self.__campus)
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Campus não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao atualizar campus.",
            )

    def deletar_campus(self) -> bool:
        try:
            if self.__campus_dao.get():
                self.__campus_dao.delete()
                logger.info(
                    "campus {} deletado com sucesso".format(
                        self.__campus.codigo
                    )
                )
                return True
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Campus não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao deletar campus.",
            )
