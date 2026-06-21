"""
extraction.py

Pulls raw, factual data out of a submitted PDF — image resolution, colour mode,
bleed presence, font embedding status. Makes no pass/fail judgements; that
decision-making lives in rules_engine.py.
"""

import fitz

#Opens the supplied PDF
def open_pdf(filepath):
    doc = fitz.open(filepath)
    results = []

#Looks at each image on each page of the PDF and captures the image composition specs to compare against the preflight_rules.yaml file 
    for page_number, page in enumerate(doc, start=1):
        bleed_data = calculate_bleed(page.trimbox, page.bleedbox)
        results.append({"page": page_number, "check_type": "bleed", "bleed_data": bleed_data})

        images = page.get_image_info(xrefs=True)
        for image in images:
            dpi = calculate_dpi(image)
            results.append({"page": page_number, "check_type": "image", "dpi": dpi, "print_mode": image["cs-name"]})
    return results

#Calculate the DPI of the supplied PDF page(s) images
def calculate_dpi(image_info):
    pixel_width = image_info["width"]
    bbox = image_info["bbox"]
    placed_width_points = bbox[2] - bbox[0]
    placed_width_inches = placed_width_points / 72
    dpi = pixel_width / placed_width_inches
    return dpi

#Calculate the amount of bleed supplied using the trimbox/bleedboxes
def calculate_bleed(trimbox, bleedbox):
    trim_width = trimbox.x1 - trimbox.x0
    trim_height = trimbox.y1 - trimbox.y0
    bleed_width = bleedbox.x1 - bleedbox.x0
    bleed_height = bleedbox.y1 - bleedbox.y0

    bleed_width_mm = (bleed_width - trim_width) / 2.835
    bleed_height_mm = (bleed_height - trim_height) / 2.835

    return{"bleed_width_mm": bleed_width_mm, "bleed_height_mm": bleed_height_mm}

if __name__ == "__main__":
    data = open_pdf("sample_pdfs/low_res_sample.pdf")
    print(data)

    doc = fitz.open("sample_pdfs/low_res_sample.pdf")
    page = doc[0]
    bleed_result = calculate_bleed(page.trimbox, page.bleedbox)
    print(bleed_result)