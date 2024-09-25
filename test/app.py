import sys
import os
import inspect

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the PDFConverter class from the pdf_to_html module
from pdf_to_html.utils import PDFConverter  # Adjust this import based on your project structure

def print_debug_message(message: str):
    """Print a debug message with the file path and line number."""
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame, 2)[1]
    file_path = caller_frame.filename
    line_number = caller_frame.lineno

    print(f"{file_path}, line {line_number}: {message}")

# Ensure this function is globally available
import builtins
builtins.print_debug_message = print_debug_message  

# Main execution starts here
if __name__ == "__main__":
    # Use raw strings (r"") or escape backslashes for Windows file paths
    converter = PDFConverter(r"C:\wamp64\RahebPDF\test\sample.pdf", r"C:\wamp64\RahebPDF\test\output.html")
    
    # Call the method to convert the PDF to HTML
    converter.convert_pdf_to_html()
    
    print_debug_message("PDF content converted and saved to output.html")
