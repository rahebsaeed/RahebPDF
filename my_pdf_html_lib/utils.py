import fitz  # PyMuPDF for PDF handling
import io
from PIL import Image

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_filename = f"page_{page_number}_img_{img_index}.png"
            
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            
            images.append(image_filename)
    
    doc.close()
    return images
def convert_text_to_html(text):
    """
    Convert extracted text to a basic HTML format.
    """
    html_content = f"<html><body><pre>{text}</pre></body></html>"
    return html_content


def save_html(html_content, output_path):
    """
    Save HTML content to a file.
    """
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

def extract_text_with_styles(pdf_path):
    text_with_styles = []
    doc = fitz.open(pdf_path)

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    for span in line['spans']:
                        text_with_styles.append({
                            "text": span['text'],
                            "font": span['font'],
                            "size": span['size'],
                            "color": span['color']
                        })
    doc.close()
    return text_with_styles

def convert_text_with_styles_to_html(text_with_styles):
    html_content = "<html><body>"

    for item in text_with_styles:
        style = f"font-family: {item['font']}; font-size: {item['size']}px; color: #{item['color']:06x};"
        # Check for bold or italic text
        if 'bold' in item['font'].lower():
            html_content += f"<b><span style='{style}'>{item['text']}</span></b>"
        elif 'italic' in item['font'].lower():
            html_content += f"<i><span style='{style}'>{item['text']}</span></i>"
        else:
            html_content += f"<span style='{style}'>{item['text']}</span>"

    html_content += "</body></html>"
    return html_content

def is_list_item(item):
    # Implement logic to detect if item is a list item
    # For example, based on text content or specific formatting
    return item['text'].startswith('- ')  # Example condition for a bullet point


def convert_lists_to_html(text_with_styles):
    html_content = "<html><body>"
    in_list = False

    for item in text_with_styles:
        # Assuming we detect list items based on some condition
        if is_list_item(item):
            if not in_list:
                html_content += "<ul>"  # Start list
                in_list = True
            html_content += f"<li>{item['text']}</li>"
        else:
            if in_list:
                html_content += "</ul>"  # End list
                in_list = False
            html_content += f"<p>{item['text']}</p>"

    if in_list:
        html_content += "</ul>"  # Close any open list

    html_content += "</body></html>"
    return html_content


def convert_tables_to_html(text_with_styles):
    html_content = "<html><body>"
    
    # Your logic to convert tables
    
    html_content += "</body></html>"
    return html_content


def convert_pdf_to_html(pdf_path, output_path):
    text_with_styles = extract_text_with_styles(pdf_path)
    
    # Convert text with styles to HTML
    html_content = convert_text_with_styles_to_html(text_with_styles)
    
    # Convert lists to HTML
    html_content = convert_lists_to_html(text_with_styles)  # Append or modify content as needed
    
    # Convert tables to HTML
    html_content += convert_tables_to_html(text_with_styles)  # Append or modify content as needed
    
    if html_content:
        save_html(html_content, output_path)
    else:
         print("Error: HTML content is None")
