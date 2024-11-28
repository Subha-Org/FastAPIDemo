import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from main import app, messages_list, MsgPayload


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_home_route(client):
    """
    Test the home route of the FastAPI application.

    This function sends a GET request to the root URL ("/") using the provided test client
    and asserts that the response status code is 200 and the response JSON matches the expected
    output.

    Args:
        client (TestClient): The test client used to make requests to the FastAPI application.

    Asserts:
        response.status_code == 200: The response status code should be 200 (OK).
        response.json() == {"message": "Hello"}: The response JSON should match the expected output.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_about_route(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the about page."}


def test_add_message(client):
    response = client.post("/messages/test_message/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"]["msg_name"] == "test_message"


def test_message_items(client):
    response = client.get("/messages")
    assert response.status_code == 200
    assert "messages:" in response.json()


def test_delete_message(client):
    # First, add a message to delete
    response = client.post("/messages/test_message_to_delete/")
    assert response.status_code == 200
    msg_id = response.json()["message"]["msg_id"]

    # Now, delete the message
    response = client.delete(f"/messages/{msg_id}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Message deleted"}

    # Verify the message is deleted
    response = client.get("/messages")
    assert response.status_code == 200
    assert msg_id not in response.json()["messages:"]