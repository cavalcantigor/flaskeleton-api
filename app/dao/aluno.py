from ..models.aluno import Aluno
from . import DAO


class AlunoDAO(DAO):
    def __init__(self, aluno: Aluno = None):
        super().__init__(aluno)

    def get_all(self) -> list:
        return self.session.query(Aluno).all()

    def get(self) -> list or Aluno:
        self.obj = (
            self.session.query(Aluno).filter_by(codigo=self.obj.codigo).first()
        )
        return self.obj
