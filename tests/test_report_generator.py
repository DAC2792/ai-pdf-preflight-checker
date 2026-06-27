import pytest
from unittest.mock import MagicMock, patch
from report_generator import generate_report, save_report

# --- generate_report Tests ---
def test_generate_report_returns_text():
    mock_response = MagicMock()
    mock_response.content[0].text = "PressLens Report: all checks passed."

    with patch("report_generator.client") as mock_client:
        mock_client.messages.create.return_value = mock_response
        result = generate_report([{"result": "pass"}], "test.pdf")

    assert "PressLens" in result

# --- save_report Tests ---
def test_save_report_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr("report_generator.BASE_DIR", tmp_path)
    output_path = save_report("Test report content", "test.pdf")
    assert output_path.exists()
    assert output_path.read_text() == "Test report content"