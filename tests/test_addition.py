from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_addition():
    response = client.post(
        "/addition/",
        json={"input_list": [1.4, 2.3, 3.2]},
    )
    assert response.status_code == 200
    assert response.json() == {"results": 6.9}
