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

#Looks at each image on each page of the PDF, calculates the DPI, saves and then produces the results
    for page_number, page in enumerate(doc, start=1):
        images = page.get_image_info(xrefs=True)
        for image in images:
            dpi = calculate_dpi(image)
            results.append({"page": page_number, "dpi": dpi, "print_mode": image["cs-name"]})

    return results

#Calculate the DPI of the supplied PDF page(s) images
def calculate_dpi(image_info):
    pixel_width = image_info["width"]
    bbox = image_info["bbox"]
    placed_width_points = bbox[2] - bbox[0]
    placed_width_inches = placed_width_points / 72
    dpi = pixel_width / placed_width_inches
    return dpi

if __name__ == "__main__":
    data = open_pdf("sample_pdfs/low_res_sample.pdf")
    print(data)