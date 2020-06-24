import pytest

from app import create_app
from app.models.db import db
from app.models.aluno import Aluno
from app.models.campus import Campus


@pytest.fixture(scope="session")
def app():
    try:
        app = create_app()

        with app.app_context():
            db.create_all()
            db.session.add(Aluno(nome="Joao da Silva", email="joaosilva@email.com"))
            db.session.add(Campus(descricao="Campus Teste"))
            db.session.commit()

        yield app

        with app.app_context():
            db.drop_all()

    except Exception as e:
        print(e)
        raise e


@pytest.fixture(scope="session")
def client(app):
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client
