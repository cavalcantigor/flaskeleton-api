from unittest.mock import patch


def test_get_docs(client):
    response = client.get('/flaskeleton-api/apidocs/')
    assert response is not None


def test_get_docs_throw_error(client):
    with patch('app.resources.docs.render_template', side_effect=Exception('Fake exception')):
        response = client.get('/flaskeleton-api/apidocs/')
        assert response.status_code == 500
        assert response.json['erro'] == "ERRO_INTERNO"
