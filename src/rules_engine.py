"""
rules_engine.py

Takes facts gathered by extraction.py and compares them against the
thresholds defined in config/preflight_rules.yaml, producing a pass/fail
verdict with supporting detail for each check.
"""

import yaml

#Open and return "Rules" for pass/fail from the preflight_rules.yaml in config
def load_rules(filepath):
    with open(filepath) as file:
        rules = yaml.safe_load(file)
    return rules

#Check resolution of the image and produce a dpi pass/fail response against the image page number
def check_resolution(dpi, page_number, rules):
    min_dpi = rules["resolution"]["min_dpi"]
    if dpi >= min_dpi:
        result = "pass"
    else:
        result = "fail"
    return {"check": "resolution", "page": page_number, "dpi": dpi, "result": result}

#Check print-mode of the image and produce a pass/fail response against the image page number
def check_colour_mode(print_mode, page_number, rules):
    required_mode = rules["colour"]["required_mode"]
    if required_mode in print_mode:
        result = "pass"
    else:
        result = "fail"
    return {"check": "colour_profile", "page": page_number, "print_mode": print_mode, "result": result}

#Calculate if there is sufficient bleed across all image points against the minimum requirement in preflight_rules.yaml     
def check_bleed(bleed_data, page_number, rules):
    width = bleed_data["bleed_width_mm"]
    height = bleed_data["bleed_height_mm"]
    min_bleed = rules["bleed"]["min_bleed_mm"]
    if width >= min_bleed and height >= min_bleed:
        result = "pass"
    else:
        result = "fail"
    return {"check": "bleed", "page": page_number, "bleed_width_mm": width, "bleed_height_mm": height, "result": result}

#Calculate if the fonts present on each page are embedded or not
def check_fonts(font_data, page_number, rules):
    require_embedded = rules["fonts"]["require_embedded"]

    all_embedded = all(font["embedded"] for font in font_data)

    if all_embedded == require_embedded:
        result = "pass"
    else:
        result = "fail"

    return {"check": "fonts", "page": page_number, "font_data": font_data, "result": result}

if __name__ == "__main__":
    rules = load_rules("config/preflight_rules.yaml")
    test_fonts = [
        {"font_name": "/F1", "base_font": "/Helvetica", "embedded": False},
        {"font_name": "/F2", "base_font": "/Helvetica-Bold", "embedded": False}
    ]
    result = check_fonts(test_fonts, 1, rules)
    print(result)