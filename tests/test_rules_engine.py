import pytest
from rules_engine import load_rules, check_resolution, check_colour_mode, check_bleed, check_fonts
from pathlib import Path

#Imports config rules from the yaml file to run tests against
@pytest.fixture
def rules():
    rules_path = Path(__file__).parent.parent / "config" / "preflight_rules.yaml"
    return load_rules(rules_path)

#--- Resolution Tests ---
def test_check_resolution_pass(rules):
    result = check_resolution(350, 1, rules)
    assert result["result"] == "pass"

def test_check_resolution_fail(rules):
    result = check_resolution(50.8, 1, rules)
    assert result["result"] == "fail"

def test_check_resolution_boundary(rules):
    result = check_resolution(300.0, 1, rules)
    assert result["result"] == "pass"

def test_check_resolution_zero_dpi(rules):
    result = check_resolution(0, 1, rules)
    assert result["result"] == "fail"

#--- Colour Mode Tests
def test_check_colour_mode_pass(rules):
    result = check_colour_mode("DeviceCMYK", 1, rules)
    assert result["result"] == "pass"

def test_check_colour_mode_fail_non_cmyk(rules):
    result = check_colour_mode("DeviceRGB", 1, rules)
    assert result["result"] == "fail"  

#--- Bleed Tests ---
def test_check_bleed_pass(rules):
    result = check_bleed({"bleed_width_mm": 3.0, "bleed_height_mm": 3.8}, 1, rules)
    assert result["result"] == "pass"

def test_check_bleed_fail(rules):
    result = check_bleed({"bleed_width_mm": 0.0, "bleed_height_mm": 0.0}, 1, rules)
    assert result["result"] == "fail"

def test_check_bleed_boundary(rules):
    result = check_bleed({"bleed_width_mm": 3.0, "bleed_height_mm": 3.0}, 1, rules)
    assert result["result"] == "pass"

#--- Font Tests ---
def test_check_fonts_pass(rules):
    result = check_fonts([{"font_name": "/F1", "base_font": "/Helvetica", "embedded": True}], 1, rules)
    assert result["result"] == "pass"

def test_check_fonts_fail(rules):
    result = check_fonts([{"font_name": "/F1", "base_font": "/Helvetica", "embedded": False}], 1, rules)
    assert result["result"] == "fail"

def test_check_fonts_mixed(rules):
    result = check_fonts([
        {"font_name": "/F1", "base_font": "/Helvetica", "embedded": True},
        {"font_name": "/F2", "base_font": "/Arial", "embedded": False}
    ], 1, rules)
    assert result["result"] == "fail"

def test_check_fonts_empty(rules):
    result = check_fonts([], 1, rules)
    assert result["result"] == "pass"