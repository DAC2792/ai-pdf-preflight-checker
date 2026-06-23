"""
main.py

Ties extraction.py and rules_engine.py together: opens a PDF, runs each
extracted image through the relevant preflight check, and reports the
pass/fail result for each one.
"""

from extraction import open_pdf
from rules_engine import load_rules, check_resolution, check_colour_mode, check_bleed, check_fonts
from report_generator import generate_report, save_report

if __name__ == "__main__":

    #Acquire results from open_pdf, and rules from the yaml file
    filepath = input("Enter the filepath to your PDF: ")
    extraction_results = open_pdf(filepath)
    rules = load_rules("config/preflight_rules.yaml")

    #List created to store all results in
    pdf_results = []

    #Loop through each image in the open_pdf extraction/rules_engine, and produce the check results
    for item in extraction_results:
        if item["check_type"] == "image":
            page_number = item["page"]
            dpi = item["dpi"]
            print_mode = item["print_mode"]
            resolution_result = check_resolution(dpi, page_number, rules)
            colour_result = check_colour_mode(print_mode, page_number, rules)
            pdf_results.append(resolution_result)
            pdf_results.append(colour_result)
        elif item["check_type"] == "bleed":
            page_number = item["page"]
            bleed_data = item["bleed_data"]
            bleed_result = check_bleed(bleed_data, page_number, rules)
            pdf_results.append(bleed_result)
        elif item["check_type"] == "fonts":
            page_number = item["page"]
            font_data = item["font_data"]
            fonts_result = check_fonts(font_data, page_number, rules)
            pdf_results.append(fonts_result)

    #Loop through all results and either Pass or Fail depending on results. Any fails will be fed back to the user along with the page location
    if all(item["result"] == "pass" for item in pdf_results):
        print("PASS - this PDF is print ready!")
    else:
        print("FAIL - this PDF is not print ready.")
        for item in pdf_results:
            if item["result"] == "fail":
                print(f" - {item['check']} failed on page {item['page']}")

    #create and print/save the final preflight report
    report = generate_report(pdf_results, filepath)
    print(report)
    save_report(report, filepath)