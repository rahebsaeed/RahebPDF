import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the PDFConverter class from the pdf_to_html module
from pdf_to_html.utils import PDFConverter

# Use raw strings (r"") or escape backslashes for Windows file paths
converter = PDFConverter(r"C:\wamp64\RahebPDF\test\sample.pdf", r"C:\wamp64\RahebPDF\test\output.html")

# Call the method to convert the PDF to HTML
converter.convert_pdf_to_html()

print("PDF content converted and saved to output.html")
