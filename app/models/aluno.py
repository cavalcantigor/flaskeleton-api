from .db import db
from . import ManagedSchema
from sqlalchemy import Column, Integer, String
from marshmallow import fields, validates, ValidationError, post_load
import re


class Aluno(db.Model):

    __tablename__ = "ALUNOS"

    codigo = Column(Integer, name="CODIGO", primary_key=True)
    nome = Column(String, name="NOME")
    email = Column(String, name="EMAIL")
    endereco = Column(String, name="ENDERECO")

    def __repr__(self):
        return "<Aluno nome={nome}, email={email}>".format(
            nome=self.nome, email=self.email
        )


class AlunoSchema(ManagedSchema):
    class Meta:
        model = Aluno

    codigo = fields.Integer()
    nome = fields.String(
        required=True,
        error_messages={"required": "`nome` é um atributo necessário."},
    )
    email = fields.String(
        required=True,
        error_messages={"required": "`email` é um atributo necessário."},
    )
    endereco = fields.String(
        required=True,
        error_messages={"required": "`endereco` é um atributo necessário."},
    )

    @post_load
    def make_user(self, data, **kwargs):
        return Aluno(**data)

    @validates("email")
    def valida_email(self, email):
        regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.search(regex, email):
            raise ValidationError("Email inválido.")
