import pytest
import io
import os
from app import app
from unittest.mock import patch
from pathlib import Path

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        yield client

#--- Happy Path Test ---
def test_check_success_path(client, tmp_path):
    """Happy path — mocks all external calls and checks /check returns 200."""
    fake_pdf = tmp_path / "test.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake")

    with patch("app.open_pdf", return_value=[
            {"check_type": "image", "page": 1, "dpi": 350, "print_mode": "DeviceCMYK"}
        ]), \
         patch("app.load_rules", return_value={"resolution": {"min_dpi": 300}, "colour": {"required_mode": "CMYK"}}), \
         patch("app.generate_report", return_value="## PressLens\nAll clear."), \
         patch("app.save_report", return_value=Path("/tmp/report.txt")):

        data = {"pdf_file": (fake_pdf.open("rb"), "test.pdf")}
        response = client.post("/check", data=data, content_type="multipart/form-data")

    assert response.status_code == 200

# --- Route Tests ---
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_check_rejects_non_pdf(client):
    """Extension filter rejects non-PDF."""
    data = {"pdf_file": (io.BytesIO(b"fake content"), "malicious.exe")}
    response = client.post("/check", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

def test_check_sanitises_path_traversal(client):
    """secure_filename strips traversal from a .pdf-named attempt."""
    from unittest.mock import patch
    app.config["PROPAGATE_EXCEPTIONS"] = False
    with patch("app.open_pdf", side_effect=Exception("not a real pdf")):
        data = {"pdf_file": (io.BytesIO(b"%PDF-1.4 fake"), "../../etc/passwd.pdf")}
        response = client.post("/check", data=data, content_type="multipart/form-data")
    assert response.status_code in (400, 500)
    assert not os.path.exists("etc/passwd.pdf")

def test_download_without_session_returns_403(client):
    response = client.get("/download")
    assert response.status_code == 403