from unittest.mock import patch

import pytest

from app.dao import DAO
from app.models.aluno import Aluno


def test_get():
    dao = DAO(Aluno())
    dao.get()
    assert isinstance(dao, DAO)


def test_insert():
    aluno = DAO(Aluno(nome="Teste")).insert()
    assert isinstance(aluno, Aluno)
    assert aluno.nome == "Teste"


def test_insert_throw_exception():
    dao = DAO(Aluno(nome="Teste"))
    with patch(
        "app.models.db.db.session.add", side_effect=Exception("Fake exception")
    ):
        with pytest.raises(Exception):
            dao.insert()


def test_update():
    aluno = DAO(Aluno(nome="Teste")).insert()
    assert isinstance(aluno, Aluno)
    aluno.email = "teste@teste.com"

    aluno_atualizado = DAO(aluno).update()
    assert isinstance(aluno_atualizado, Aluno)
    assert aluno_atualizado.email == "teste@teste.com"


def test_update_throw_exception():
    dao = DAO(Aluno(nome="Teste"))
    with patch(
        "app.models.db.db.session.add", side_effect=Exception("Fake exception")
    ):
        with pytest.raises(Exception):
            dao.update()


def test_delete():
    aluno = DAO(Aluno(nome="Teste")).insert()
    assert isinstance(aluno, Aluno)
    assert DAO(aluno).delete()


def test_delete_throw_exception():
    dao = DAO(Aluno(nome="Teste"))
    with patch(
        "app.models.db.db.session.delete",
        side_effect=Exception("Fake exception"),
    ):
        with pytest.raises(Exception):
            dao.delete()
