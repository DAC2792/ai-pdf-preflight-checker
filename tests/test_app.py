import pytest
import io
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        yield client

# --- Route Tests ---
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_check_rejects_non_pdf(client):
    data = {"pdf_file": (io.BytesIO(b"fake content"), "malicious.exe")}
    response = client.post("/check", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

def test_check_rejects_path_traversal(client):
    data = {"pdf_file": (io.BytesIO(b"fake content"), "../../app.py")}
    response = client.post("/check", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

def test_download_without_session_returns_403(client):
    response = client.get("/download")
    assert response.status_code == 403