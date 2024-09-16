import pdfplumber
from bs4 import BeautifulSoup

# Function to convert list of lists to HTML table with <thead> and <tbody>
def list_to_html_table(data):
    html_table = "<table>\n"
    
    # Detect headers (using the first row as headers)
    headers = data[0]
    html_table += "  <thead>\n    <tr>\n"
    for header in headers:
        html_table += f"      <th>{header}</th>\n"
    html_table += "    </tr>\n  </thead>\n"
    
    # Add the rest of the rows as table body
    html_table += "  <tbody>\n"
    for row in data[1:]:
        html_table += "    <tr>\n"
        for cell in row:
            html_table += f"      <td>{cell}</td>\n"
        html_table += "    </tr>\n"
    html_table += "  </tbody>\n"
    
    html_table += "</table>"
    return html_table

# PDF file path
pdf_file = r"C:\wamp64\RahebPDF\test\resarch.pdf"

# Extract tables from the PDF using pdfplumber
pdf = pdfplumber.open(pdf_file)
html_tables = []

for page in pdf.pages:
    page_tables = page.extract_tables()
    for table_data in page_tables:
        num_rows = len(table_data)
        num_cols = max(len(row) for row in table_data)
        cell_data = [[''] * num_cols for _ in range(num_rows)]

        for i, row in enumerate(table_data):
            for j, cell in enumerate(row):
                if cell:
                    # Detect headers (first row)
                    if i == 0:
                        cell_text = f'<th>{cell}</th>'
                    else:
                        cell_text = f'<td>{cell}</td>'
                    
                    cell_data[i][j] = cell_text

        # Convert the data into an HTML table
        html_table = list_to_html_table(cell_data)
        html_tables.append(html_table)

# Combine all HTML tables into a single HTML document
output_html = "\n".join(html_tables)

# Parse the HTML to beautify it
soup = BeautifulSoup(output_html, 'html.parser')
pretty_html = soup.prettify()

# Print or save the prettified HTML output as needed
print(pretty_html)

# Save the HTML table to a file or print it as needed
with open('table.html', 'w', encoding='utf-8') as html_file:
    html_file.write(pretty_html)
