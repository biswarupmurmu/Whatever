import pytest

from ourapp import create_app
app = create_app()

@pytest.fixture
def client():
    """
    Fixture to set up a test client for the Flask application.

    Yields:
        FlaskClient: A test client for making requests to the Flask application.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """
    Test case to verify the status code of the homepage.

    Args:
        client (FlaskClient): The test client for making requests.

    Assertion:
        Asserts that the response status code is 200.
    """
    response = client.get("/")
    assert response.status_code == 200

def test_homepage_content(client):
    """
    Test case to verify the content of the homepage.

    Args:
        client (FlaskClient): The test client for making requests.

    Assertion:
        Asserts that the response data contains the specified content.
    """
    response = client.get("/")
    assert b"Whatever" in response.data
    
if __name__ == "__main__":
    pytest.main()