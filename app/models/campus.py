from marshmallow import fields, post_load
from sqlalchemy import Column, Integer, String

from . import ManagedSchema
from .db import db


class Campus(db.Model):

    __tablename__ = "CAMPUS"

    codigo = Column(Integer, name="CODIGO", primary_key=True)
    descricao = Column(String, name="DESCRICAO")

    def __repr__(self):
        return "<Campus descricao={descricao}>".format(
            descricao=self.descricao
        )


class CampusSchema(ManagedSchema):
    class Meta:
        model = Campus

    codigo = fields.Integer()
    descricao = fields.String(
        required=True,
        error_messages={"required": "`descricao` é um atributo necessário."},
    )

    @post_load
    def make_user(self, data, **kwargs):
        return Campus(**data)
