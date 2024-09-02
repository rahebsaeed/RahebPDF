import fitz  # PyMuPDF for PDF handling
import io
from PIL import Image


def extract_text_with_styles(pdf_path):
    text_with_styles = []
    doc = fitz.open(pdf_path)

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    for span in line['spans']:
                        # Extract detailed style information
                        text_with_styles.append({
                            "text": span['text'],
                            "font": span['font'],
                            "size": span['size'],
                            "color": span['color'],
                            "flags": span['flags']  # To detect bold, italic
                        })
    doc.close()
    return text_with_styles


def generate_css(text_with_styles):
    css = "<style>"
    classes = {}
    class_counter = 0

    # Create CSS classes for each style
    for item in text_with_styles:
        # Create a unique style key
        style_key = (item['font'], item['size'], item['color'], item['flags'])
        if style_key not in classes:
            class_name = f"text-style-{class_counter}"
            classes[style_key] = class_name
            class_counter += 1

            # Check for bold and italic flags
            font_weight = "bold" if item['flags'] & 2 else "normal"
            font_style = "italic" if item['flags'] & 1 else "normal"

            # Convert the color from integer to hex
            color = f"#{item['color']:06x}"

            # Create the CSS rule
            css += f"""
            .{class_name} {{
                font-family: '{item['font']}';
                font-size: {item['size']}px;
                color: {color};
                font-weight: {font_weight};
                font-style: {font_style};
            }}
            """
    
    css += "</style>"
    return css, classes


def convert_text_with_styles_to_html(text_with_styles):
    html_content = "<html><head>"

    # Generate CSS and get class mapping
    css, classes = generate_css(text_with_styles)
    html_content += css + "</head><body>"

    # Group spans into paragraphs
    current_paragraph = []

    for index, item in enumerate(text_with_styles):
        class_name = classes[(item['font'], item['size'], item['color'], item['flags'])]
        span = f"<span class='{class_name}'>{item['text']}</span>"

        # Detect line breaks or paragraph separations
        if item['text'].endswith('\n') or item['text'].strip() == '':
            if current_paragraph:  # If there's content collected, wrap it in a paragraph
                html_content += f"<p>{''.join(current_paragraph)}</p>"
                current_paragraph = []  # Reset for the next paragraph
        else:
            current_paragraph.append(span)

    # Add the last paragraph if it exists
    if current_paragraph:
        html_content += f"<p>{''.join(current_paragraph)}</p>"

    html_content += "</body></html>"
    return html_content


def save_html(html_content, output_path):
    """
    Save HTML content to a file.
    """
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)


def convert_pdf_to_html(pdf_path, output_path):
    text_with_styles = extract_text_with_styles(pdf_path)
    html_content = convert_text_with_styles_to_html(text_with_styles)
    save_html(html_content, output_path)

