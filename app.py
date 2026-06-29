"""
PressLens webapp. This is the online 'face' of the program. Use to activate the PressLens webapp
to which you can upload PDFs, generate and download print readiness preflight reports,
and run multiple checks on multiple files. All from the custom styled PressLens interface.
"""

import os
from flask import Flask, render_template, request, session, abort, send_file
from extraction import open_pdf
from report_generator import generate_report, save_report
from rules_engine import check_resolution, check_colour_mode, check_bleed, check_fonts, load_rules
from pathlib import Path
from dotenv import load_dotenv
import markdown
from werkzeug.utils import secure_filename
import bleach
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#runs all pathing from the required parent folder or 'root'
BASE_DIR = Path(__file__).parent

#assign specific tags/extensions to work alongside bleach to prevent XSS (cross-site scripting). blocking users from injecting malicous scripts
ALLOWED_TAGS = [
    "h1", "h2", "h3", "p", "ul", "ol", "li",
    "strong", "em", "code", "pre", "hr",
    "table", "thead", "tbody", "tr", "th", "td"
    ]

ALLOWED_EXTENSIONS = {"pdf"}
_report_store: dict[str, str] = {}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

#load environment variables (.env read, create Flask app, assign secret key encryption)
load_dotenv()
app = Flask(__name__)
secret_key = os.getenv("FLASK_SECRET_KEY")
if not secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is not set. Add it to your .env file.")
app.secret_key = secret_key

#Limits upload size to 50MB to prevent memory exhustion / DoS attacks
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

@app.errorhandler(413)
def file_too_large(e):
    abort(400, "File exceeds the 50 MB upload limit.")

# rate limiter - prevents API quota exhaustion from repeated requests
limiter = Limiter(get_remote_address, app = app, default_limits=["10 per minute"])

#route to the HTML home page
@app.route("/")
def home():
    return render_template("index.html")

#create report and route the user to the results page. Security restrictions included to prevent malicous filenames from overwriting outside of intended parameters
@app.route("/check", methods=["POST"])
@limiter.limit("10 per minute")
def check():
    file = request.files.get("pdf_file")
    if not file or file.filename == "":
        abort(400, "No file provided.")
    filename = secure_filename(file.filename)
    if not filename:
        abort(400, "Invalid filename.")
    if not allowed_file(filename):
        abort(400, "Only PDF files are accepted.")
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    upload_dir = BASE_DIR / "sample_pdfs"
    upload_dir.mkdir(exist_ok = True)
    filepath = upload_dir / unique_filename
    file.save(filepath)

    #try/finally runs the logic, and finally deletes the uploaded PDF from sample_pdfs/
    try:
        extraction_results = open_pdf(filepath)
        rules = load_rules(BASE_DIR / "config" / "preflight_rules.yaml")

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

        report_html = bleach.clean(markdown.markdown(report), tags=ALLOWED_TAGS, strip=True)
        report_key = uuid.uuid4().hex
        _report_store[report_key] = str(report_path)
        session["report_key"] = report_key
        return render_template("results.html", report = report_html, overall_pass = overall_pass, filename = filename)
    finally:
        try:
            filepath.unlink(missing_ok = True)
        except PermissionError:
            pass

#download function for the generated report
@app.route("/download")
def download():
    report_key = session.get("report_key")
    report_path = _report_store.get(report_key) if report_key else None
    if not report_path:
        abort(403, "No report available.")
    return send_file(report_path, as_attachment = True)

if __name__ == "__main__":
    app.run(debug = os.getenv("FLASK_DEBUG", "false").lower() == "true")