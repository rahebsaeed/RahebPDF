# Use the correct package name as defined in your project
from my_pdf_html_lib.utils import extract_text_from_pdf, extract_images_from_pdf

# Example usage
pdf_path = 'sample.pdf'
text = extract_text_from_pdf(pdf_path)
print("Extracted Text:", text)

images = extract_images_from_pdf(pdf_path)
print("Extracted Images:", images)
