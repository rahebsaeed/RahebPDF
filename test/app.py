from my_pdf_html_lib.pdf_to_html import convert_pdf_to_html

pdf_path = "sample.pdf"
html_content = convert_pdf_to_html(pdf_path)

with open("output.html", "w") as file:
    file.write(html_content)
