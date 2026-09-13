import app as api


def test_home_includes_author(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["author"] == "Ahmed Hassan"


def test_health_reports_database_status(client, monkeypatch):
    monkeypatch.setattr(api, "database_status", lambda: "connected")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok", "database": "connected"}


def test_products_returns_database_rows(client, monkeypatch):
    class Cursor:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def execute(self, query):
            assert "FROM products" in query

        def fetchall(self):
            return [(1, "Docker practice course", 2500)]

    class Connection:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def cursor(self):
            return Cursor()

    monkeypatch.setattr(api.psycopg, "connect", lambda **kwargs: Connection())

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "Docker practice course", "price_cents": 2500}]


import pytest


@pytest.fixture
def client():
    api.app.config.update(TESTING=True)
    return api.app.test_client()
