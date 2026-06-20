"""
main.py

Ties extraction.py and rules_engine.py together: opens a PDF, runs each
extracted image through the relevant preflight check, and reports the
pass/fail result for each one.
"""

from extraction import open_pdf
from rules_engine import load_rules, check_resolution

if __name__ == "__main__":

    #Acquire results from open_pdf, and rules from the yaml file
    extraction_results = open_pdf("sample_pdfs/low_res_sample.pdf")
    rules = load_rules("config/preflight_rules.yaml")

    #Loop through each image in the open_pdf extraction, and produce the dpi check results
    for item in extraction_results:
        page_number = item["page"]
        dpi = item["dpi"]
        result = check_resolution(dpi, page_number, rules)
        print(result)