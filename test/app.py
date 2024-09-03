import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the function from the pdf_to_html module
from pdf_to_html.utils import convert_pdf_to_html

# Convert PDF to HTML and save it
convert_pdf_to_html("sample.pdf", "output.html")

print("PDF content converted and saved to output.html")
