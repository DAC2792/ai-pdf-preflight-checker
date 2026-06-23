import pytest
import sys
import os

#checks inside the src folder for all the required functions to import for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rules_engine import load_rules, check_resolution, check_colour_mode, check_bleed, check_fonts

#amendable test functions
def test_check_resolution_pass():
    rules = {"resolution": {"min_dpi": 300}}
    result = check_resolution(350, 1, rules)
    assert result["result"] == "pass"

def test_check_resolution_fail():
    rules = {"resolution": {"min_dpi": 300}}
    result = check_resolution(50.8, 1, rules)
    assert result["result"] == "fail"

def test_check_colour_mode_pass():
    rules = {"colour": {"required_mode": "CMYK"}}
    result = check_colour_mode("DeviceCMYK", 1, rules)
    assert result["result"] == "pass"

def test_check_colour_mode_fail():
    rules = {"colour": {"required_mode": "CMYK"}}
    result = check_colour_mode("DeviceRGB", 1, rules)
    assert result["result"] == "fail"

def test_check_bleed_pass():
    rules = {"bleed": {"min_bleed_mm": 3}}
    result = check_bleed({"bleed_width_mm": 3.0, "bleed_height_mm": 3.8}, 1, rules)
    assert result["result"] == "pass"

def test_check_bleed_fail():
    rules = {"bleed": {"min_bleed_mm": 3}}
    result = check_bleed({"bleed_width_mm": 0.0, "bleed_height_mm": 0.0}, 1, rules)
    assert result["result"] == "fail"

def test_check_fonts_pass():
    rules = {"fonts": {"require_embedded": True}}
    result = check_fonts([{"font_name": "/F1", "base_font": "/Helvetica", "embedded": True}], 1, rules)
    assert result["result"] == "pass"

def test_check_fonts_fail():
    rules = {"fonts": {"require_embedded": True}}
    result = check_fonts([{"font_name": "/F1", "base_font": "/Helvetica", "embedded": False}], 1, rules)
    assert result["result"] == "fail"