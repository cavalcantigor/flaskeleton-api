from .db import db, ma
from sqlalchemy import Column, Integer, String
from marshmallow import fields, validates, ValidationError
import re


class Aluno(db.Model):

    __tablename__ = "ALUNOS"

    codigo = Column(Integer, name="CODIGO", primary_key=True)
    nome = Column(String, name="NOME")
    email = Column(String, name="EMAIL")
    endereco = Column(String, name="ENDERECO")

    def __repr__(self):
        return "<Aluno codigo={codigo}, nome={nome}, email={email}>".format(
            codigo=self.codigo, nome=self.nome, email=self.email
        )


class AlunoSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Aluno
        sqla_session = db.session

    codigo = fields.Integer(dump_only=True)
    nome = fields.String(required=True, error_messages={"required": "`nome` é um atributo necessário."})
    email = fields.String(required=True, error_messages={"required": "`email` é um atributo necessário."})
    endereco = fields.String(required=True, error_messages={"required": "`endereco` é um atributo necessário."})

    @validates("email")
    def valida_email(self, email):
        regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.search(regex, email):
            raise ValidationError("Email inválido.")

