import pytest
from rules_engine import load_rules, check_resolution, check_colour_mode, check_bleed, check_fonts

#--- Resolution Tests ---
def test_check_resolution_pass():
    rules = {"resolution": {"min_dpi": 300}}
    result = check_resolution(350, 1, rules)
    assert result["result"] == "pass"

def test_check_resolution_fail():
    rules = {"resolution": {"min_dpi": 300}}
    result = check_resolution(50.8, 1, rules)
    assert result["result"] == "fail"

def test_check_resolution_boundary():
    rules = {"resolution": {"min_dpi": 300}}
    result = check_resolution(300.0, 1, rules)
    assert result["result"] == "pass"

def test_check_resolution_zero_dpi():
    rules = {"resolution": {"min_dpi": 300}}
    result = check_resolution(0, 1, rules)
    assert result["result"] == "fail"

#--- Colour Mode Tests
def test_check_colour_mode_pass():
    rules = {"colour": {"required_mode": "CMYK"}}
    result = check_colour_mode("DeviceCMYK", 1, rules)
    assert result["result"] == "pass"

def test_check_colour_mode_fail_non_cmyk():
    rules = {"colour": {"required_mode": "CMYK"}}
    result = check_colour_mode("DeviceRGB", 1, rules)
    assert result["result"] == "fail"  

#--- Bleed Tests ---
def test_check_bleed_pass():
    rules = {"bleed": {"min_bleed_mm": 3}}
    result = check_bleed({"bleed_width_mm": 3.0, "bleed_height_mm": 3.8}, 1, rules)
    assert result["result"] == "pass"

def test_check_bleed_fail():
    rules = {"bleed": {"min_bleed_mm": 3}}
    result = check_bleed({"bleed_width_mm": 0.0, "bleed_height_mm": 0.0}, 1, rules)
    assert result["result"] == "fail"

def test_check_bleed_boundary():
    rules = {"bleed": {"min_bleed_mm": 3}}
    result = check_bleed({"bleed_width_mm": 3.0, "bleed_height_mm": 3.0}, 1, rules)
    assert result["result"] == "pass"

#--- Font Tests ---
def test_check_fonts_pass():
    rules = {"fonts": {"require_embedded": True}}
    result = check_fonts([{"font_name": "/F1", "base_font": "/Helvetica", "embedded": True}], 1, rules)
    assert result["result"] == "pass"

def test_check_fonts_fail():
    rules = {"fonts": {"require_embedded": True}}
    result = check_fonts([{"font_name": "/F1", "base_font": "/Helvetica", "embedded": False}], 1, rules)
    assert result["result"] == "fail"

def test_check_fonts_mixed():
    rules = {"fonts": {"require_embedded": True}}
    result = check_fonts([
        {"font_name": "/F1", "base_font": "/Helvetica", "embedded": True},
        {"font_name": "/F2", "base_font": "/Arial", "embedded": False}
    ], 1, rules)
    assert result["result"] == "fail"

def test_check_fonts_empty():
    rules = {"fonts": {"require_embedded": True}}
    result = check_fonts([], 1, rules)
    assert result["result"] == "pass"