import pytest
from extraction import calculate_dpi, calculate_bleed, check_font_embedding

# --- DPI Tests ---
def test_calculate_dpi_normal():
    image_info = {"width": 2480, "height": 3508, "bbox": (0, 0, 595, 842)}
    result = calculate_dpi(image_info)
    assert result > 0

def test_calculate_dpi_zero_width():
    # zero-width bounding box should return 0, not crash
    image_info = {"width": 2480, "height": 3508, "bbox": (0, 0, 0, 842)}
    result = calculate_dpi(image_info)
    assert result == 0

# --- Bleed Tests ---
def test_calculate_bleed_normal():
    class Box:
        def __init__(self, x0, y0, x1, y1):
            self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

    trimbox = Box(0, 0, 210, 297)
    bleedbox = Box(-8.5, -8.5, 218.5, 305.5)
    result = calculate_bleed(trimbox, bleedbox)
    assert result["bleed_width_mm"] > 0
    assert result["bleed_height_mm"] > 0

# --- Font Embedding Tests ---
def test_check_font_embedding_embedded():
    from unittest.mock import MagicMock
    mock_page = MagicMock()
    mock_page.Resources = {
        "/Font": {
            "/F1": {
                "/BaseFont": "/Helvetica",
                "/FontDescriptor": {"/FontFile2": MagicMock()},
            }
        }
    }
    result = check_font_embedding(mock_page)
    assert result[0]["embedded"] is True

def test_check_font_embedding_not_embedded():
    from unittest.mock import MagicMock
    mock_page = MagicMock()
    mock_page.Resources = {
        "/Font": {
            "/F1": {"/BaseFont": "/Helvetica", "/FontDescriptor": {}}
        }
    }
    result = check_font_embedding(mock_page)
    assert result[0]["embedded"] is False