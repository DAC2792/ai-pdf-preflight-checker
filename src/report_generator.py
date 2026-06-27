"""
report_generator.py

Takes the structured preflight check results from rules_engine.py and uses
the Claude API to generate a clear, professional, human-readable report.
Explains which checks passed or failed, why each failure matters for print
production, and what the customer needs to fix.
"""

import anthropic
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

#load the .env file details into the program (keeps them private and secure)
load_dotenv()

#runs all pathing from the required parent folder or 'root'
BASE_DIR = Path(__file__).parent

#call into anthropic using the API key within the .env file. Error handling in place if the key is not found/recognised
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")

client = anthropic.Anthropic(api_key = api_key)

#generate a human-readable preflight report using the anthropic API
def generate_report(pdf_results, filepath):
    message = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 2048,
        messages = [
            {"role": "user", "content": f"""You are a professional print production specialist. You are acting for a software application named "PressLens" which is built to help support users in selecting print ready artwork.
            Below are the preflight check results for a PDF file. Which tell us if a file is print ready or not.
            Begin the report with a PressLens header, and sign off as PressLens at the end.
            Write a clear, concise preflight report - no longer than one page.
            Use plain English that anyone can understand, not just print professionals.
            For each issue explain:
            - What failed and why it matters in simple terms
            - One clear action the customer needs to take to fix it
             
            PDF file: {filepath}
            Results: {pdf_results}"""}
        ]
    )
    return(message.content[0].text)

#save the report into outputs using the filename and datetime as the naming convention
def save_report(report_text, filepath):
    pdf_name = os.path.splitext(os.path.basename(filepath))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    #ensures outputs folder exists before running. if not, it is created
    output_dir = BASE_DIR / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_filename = output_dir / f"PressLens_report_{pdf_name}_{timestamp}.txt"

    with open(output_filename, "w", encoding = "utf-8") as f:
        f.write(report_text)

    print(f"Report saved to: {output_filename}")
    return output_filename