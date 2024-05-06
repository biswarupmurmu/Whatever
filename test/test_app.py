import pytest

from ourapp import create_app
app = create_app()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200

def test_homepage_content(client):
    response = client.get("/")
    assert b"Whatever" in response.data
    
if __name__ == "__main__":
    pytest.main()