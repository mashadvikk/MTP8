import pytest
from fastapi.testclient import TestClient

from mvc_calc.api import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_calculate(client):
    response = client.post("/calculations", json={"expression": "2+3*4"})
    assert response.status_code == 201
    assert response.json() == {"expression": "2+3*4", "result": 14}


@pytest.mark.parametrize("expression, message", [
    ("1/0", "деление на ноль"), ("2+", "выражение не закончено")])
def test_calculation_error(client, expression, message):
    response = client.post("/calculations", json={"expression": expression})
    assert response.status_code == 400
    assert response.json() == {"detail": message}


@pytest.mark.parametrize("body", [
    {}, {"expression": ""}, {"expression": 5}, {"expression": "(" * 5000}])
def test_wrong_request(client, body):
    assert client.post("/calculations", json=body).status_code == 422


def test_history(client):
    assert client.get("/calculations").json() == []
    for expression in ("1+1", "1/0", "ans*10"):
        client.post("/calculations", json={"expression": expression})
    assert client.get("/calculations").json() == [
        {"expression": "1+1", "result": 2},
        {"expression": "ans*10", "result": 20}]


def test_clear_history(client):
    client.post("/calculations", json={"expression": "1+1"})
    assert client.delete("/calculations").status_code == 204
    assert client.get("/calculations").json() == []


def test_applications_do_not_share_history(client):
    client.post("/calculations", json={"expression": "1+1"})
    assert TestClient(create_app()).get("/calculations").json() == []


def test_documentation(client):
    schema = client.get("/openapi.json").json()
    assert set(schema["paths"]["/calculations"]) == {"get", "post", "delete"}
