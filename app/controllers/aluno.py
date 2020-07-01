from marshmallow import ValidationError

from ..commons.logger import logger
from ..dao.aluno import AlunoDAO
from ..errors import ErroInterno, TipoErro, UsoInvalido
from ..models.aluno import Aluno, AlunoSchema


class AlunoController:
    def __init__(self, codigo: int = None):
        self.__aluno_schema = AlunoSchema()
        self.__aluno = Aluno(codigo=codigo)
        self.__aluno_dao = AlunoDAO(self.__aluno)

    def recuperar_aluno(self) -> list or Aluno:
        try:
            if self.__aluno.codigo:
                self.__aluno = self.__aluno_dao.get()
                if self.__aluno:
                    logger.info(
                        "aluno {} recuperado(s) com sucesso".format(
                            self.__aluno.codigo
                        )
                    )
                    return self.__aluno_schema.dump(self.__aluno)
                else:
                    raise UsoInvalido(
                        TipoErro.NAO_ENCONTRADO.name,
                        payload="Aluno não foi encontrado.",
                        status_code=404,
                    )
            else:
                return self.__aluno_schema.dump(
                    self.__aluno_dao.get_all(), many=True
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao recuperar aluno(s).",
            )

    def criar_aluno(self, aluno: dict = None) -> Aluno:
        try:
            self.__aluno = self.__aluno_schema.load(
                aluno, instance=self.__aluno
            )
            self.__aluno_dao = AlunoDAO(self.__aluno)
            self.__aluno_dao.insert()
            logger.info(
                "aluno {} criado com sucesso".format(str(self.__aluno))
            )
            return self.__aluno_schema.dump(self.__aluno)
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
                payload="Ocorreu um erro ao criar aluno." + str(e),
            )

    def atualizar_aluno(self, dados_aluno: dict = None) -> Aluno:
        try:
            self.__aluno = self.__aluno_dao.get()
            if self.__aluno:
                erros = self.__aluno_schema.validate(dados_aluno)
                if erros:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name, payload=str(erros)
                    )
                self.__aluno_schema.update(self.__aluno, dados_aluno)
                self.__aluno = self.__aluno_dao.update()
                logger.info(
                    "aluno {} atualizado com sucesso".format(
                        self.__aluno.codigo
                    )
                )
                return self.__aluno_schema.dump(self.__aluno)
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
                payload="Ocorreu um erro ao atualizar aluno.",
            )

    def deletar_aluno(self) -> bool:
        try:
            if self.__aluno_dao.get():
                self.__aluno_dao.delete()
                logger.info(
                    "aluno {} deletado com sucesso".format(self.__aluno.codigo)
                )
                return True
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
                payload="Ocorreu um erro ao deletar aluno.",
            )
