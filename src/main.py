"""
main.py

Ties extraction.py and rules_engine.py together: opens a PDF, runs each
extracted image through the relevant preflight check, and reports the
pass/fail result for each one.
"""

from extraction import open_pdf
from rules_engine import load_rules, check_resolution, check_colour_mode, check_bleed

if __name__ == "__main__":

    #Acquire results from open_pdf, and rules from the yaml file
    extraction_results = open_pdf("sample_pdfs/low_res_sample.pdf")
    rules = load_rules("config/preflight_rules.yaml")

    #Loop through each image in the open_pdf extraction, and produce the check results
    for item in extraction_results:
        if item["check_type"] == "image":
            page_number = item["page"]
            dpi = item["dpi"]
            print_mode = item["print_mode"]
            resolution_result = check_resolution(dpi, page_number, rules)
            colour_result = check_colour_mode(print_mode, page_number, rules)
            print(resolution_result)
            print(colour_result)
        elif item["check_type"] == "bleed":
            page_number = item["page"]
            bleed_data = item["bleed_data"]
            bleed_result = check_bleed(bleed_data, page_number, rules)
            print(bleed_result)
