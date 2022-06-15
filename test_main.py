from fastapi.testclient import TestClient
from product.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/product")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello!"}
