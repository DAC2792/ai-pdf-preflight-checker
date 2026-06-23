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

#load the .env file details into the program (keeps them private and secure)
load_dotenv()

#call into anthropic using the API key within the .env file
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

#generate a human-readable preflight report using the anthropic API
def generate_report(pdf_results, filepath):
    message = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 2048,
        messages = [
            {"role": "user", "content": f"""You are a professional print production specialist. You are acting for a software application named "PressLens" which is built to help support users in selecting print ready artwork.
            Below are the preflight check results for a PDF file. Which tell us if a file is print ready or not.
            Begin the report with a PressLens header, and sign off as PressLens at the end.
            Write a clear, professional preflight report explaining:
            - Which checks passed and which failed
            - Why each failure matters for print production
            - What the customer needs to fix
             
            PDF file: {filepath}
            Results: {pdf_results}"""}
        ]
    )
    return(message.content[0].text)