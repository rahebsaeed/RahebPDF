from RahebPDF.utils import extract_text_with_styles, convert_text_with_styles_to_html, save_html, convert_pdf_to_html

# Convert PDF to HTML and save it
convert_pdf_to_html("sample.pdf", "output.html")

print("PDF content converted and saved to output.html")
