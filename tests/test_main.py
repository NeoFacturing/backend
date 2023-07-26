import pytest
from fastapi.testclient import TestClient
from app.main import app  # replace with the actual path to your FastAPI app
import tempfile
import os


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
