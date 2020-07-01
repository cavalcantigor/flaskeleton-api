from flask import g
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


class MultiTenantSQLAlchemy(SQLAlchemy):
    """
        Implementation from:
        https://quanttype.net/posts/2016-03-15-flask-sqlalchemy-and-multitenancy.html
    """

    @staticmethod
    def choose_tenant(bind_key):
        if hasattr(g, "tenant"):
            raise RuntimeError(
                "Switching tenant in the middle of the request."
            )
        g.tenant = bind_key

    def get_engine(self, app=None, bind=None):
        if hasattr(g, "tenant"):
            bind = g.tenant
        return super().get_engine(app=app, bind=bind)


db = MultiTenantSQLAlchemy()
ma = Marshmallow()
