import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, render_template, request, session, redirect, url_for
from extraction import open_pdf
from report_generator import generate_report, save_report
from rules_engine import check_resolution, check_colour_mode, check_bleed, check_fonts, load_rules
from dotenv import load_dotenv
import markdown

#load environment variables (.env read, create Flask app, assign secret key encryption)
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

#route to the HTML home page
@app.route("/")
def home():
    return render_template("index.html")

#create report and route the user to the results page
@app.route("/check", methods=["POST"])
def check():
    file = request.files["pdf_file"]
    filepath = os.path.join("sample_pdfs", file.filename)
    file.save(filepath)

    extraction_results = open_pdf(filepath)
    rules = load_rules("config/preflight_rules.yaml")

    pdf_results = []
    for item in extraction_results:
        if item["check_type"] == "image":
            page_number = item["page"]
            dpi = item["dpi"]
            print_mode = item["print_mode"]
            pdf_results.append(check_resolution(dpi, page_number, rules))
            pdf_results.append(check_colour_mode(print_mode, page_number, rules))
        elif item["check_type"] == "bleed":
            pdf_results.append(check_bleed(item["bleed_data"], item["page"], rules))
        elif item["check_type"] == "fonts":
            pdf_results.append(check_fonts(item["font_data"], item["page"], rules))

    overall_pass = all(item["result"] == "pass" for item in pdf_results)
    report = generate_report(pdf_results, filepath)
    report_path = save_report(report, filepath)

    report_html = markdown.markdown(report)
    return render_template("results.html", report = report_html, overall_pass = overall_pass, filename = file.filename, report_path = report_path)

#results page supplies the finished report
@app.route("/results")
def results():
    report = session.get("report", "")
    overall_pass = session.get("overall_pass", False)
    filename = session.get("filename", "")
    return render_template("results.html", report = report, overall_pass = overall_pass, filename = filename)

#download function for the generated report
@app.route("/download")
def download():
    from flask import send_file
    report_path = request.args.get("path")
    return send_file(report_path, as_attachment = True)

if __name__ == "__main__":
    app.run(debug = True)