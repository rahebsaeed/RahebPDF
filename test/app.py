# Import your library
from my_pdf_html_lib import convert_pdf_to_html, convert_html_to_pdf

# Example usage
pdf_path = 'sample.pdf'
html_output = convert_pdf_to_html(pdf_path)

# Save HTML output to a file
with open('output.html', 'w') as file:
    file.write(html_output)

# Converting HTML back to PDF (example)
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
convert_html_to_pdf(html_content, 'output.pdf')
