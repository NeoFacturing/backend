import pytest
from fastapi.testclient import TestClient
from app.main import app, read_chat
import asyncio
import os
import tempfile
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.database.schemas import ChatRequest, Message


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def test_file():
    file_content = b"Some file content"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp:
        tmp.write(file_content)
        yield tmp.name
    # Cleanup: remove the temporary file
    if os.path.exists(tmp.name):
        os.remove(tmp.name)


def test_upload_file(test_client, test_file):
    # Open the temporary file and send a request to the endpoint
    with open(test_file, "rb") as f:
        response = test_client.post(
            "/uploadfile", files={"file": ("test.step", f, "application/step")}
        )

    # Check the status code of the response
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    # Check the contents of the response
    assert "filename" in response.json(), "Response does not contain 'filename'"

    # Cleanup: remove the uploaded file
    if os.path.exists("docs/test.step"):
        os.remove("docs/test.step")


def test_read_chat():
    # create a mock request
    mock_request = ChatRequest(
        messages=[Message(role="user", content="Hello, AI!")], files=["test.step"]
    )
    # Mock the get_response function to return a response
    with patch(
        "app.main.get_response", return_value="Hello, user!"
    ) as mock_get_response:
        response = asyncio.run(read_chat(mock_request))
        assert response == "Hello, user!"
        mock_get_response.assert_called_once_with(
            "Hello, AI!", ai="qa-chain", input_file="test.step"
        )

    # Mock the get_response function to raise an Exception
    with patch("app.main.get_response", side_effect=Exception()) as mock_get_response:
        with pytest.raises(HTTPException) as excinfo:
            asyncio.run(read_chat(mock_request))
        assert excinfo.value.status_code == 500
        print(f"HTTPException detail: {excinfo.value.detail}")
        mock_get_response.assert_called_once_with(
            "Hello, AI!", ai="qa-chain", input_file="test.step"
        )
