from my_pdf_html_lib.utils import extract_text_from_pdf, convert_text_to_html, save_html

# Extract text from PDF
extracted_text = extract_text_from_pdf("path/to/your.pdf")

# Convert text to HTML
html_content = convert_text_to_html(extracted_text)

# Save HTML to a file
save_html(html_content, "output.html")

print("PDF content converted and saved to output.html")
