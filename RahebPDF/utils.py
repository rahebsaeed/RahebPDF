import fitz  # PyMuPDF for PDF handling
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()


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
                            "flags": span['flags'],  # To detect bold, italic
                            "alignment": block.get('alignment', 0),  # Alignment info
                            "bbox": block.get('bbox', (0, 0, 0, 0))  # Bounding box for padding/margin
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
        style_key = (item['font'], item['size'], item['color'], item['flags'], item['alignment'])
        if style_key not in classes:
            class_name = f"text-style-{class_counter}"
            classes[style_key] = class_name
            class_counter += 1

            # Check for bold and italic flags
            font_weight = "bold" if item['flags'] & 2 else "normal"
            font_style = "italic" if item['flags'] & 1 else "normal"

            # Convert the color from integer to hex
            color = f"#{item['color']:06x}"

            # Set text alignment
            align_map = {0: 'left', 1: 'center', 2: 'right', 3: 'justify'}
            text_align = align_map.get(item['alignment'], 'left')

            # Extract padding/margin from bounding box
            top, left, bottom, right = item['bbox']

            # Create the CSS rule
            css += f"""
            .{class_name} {{
                font-family: '{item['font']}';
                font-size: {item['size']}px;
                color: {color};
                font-weight: {font_weight};
                font-style: {font_style};
                text-align: {text_align};
                margin: {top}px {right}px {bottom}px {left}px;
            }}
            """
    
    css += "</style>"
    return css, classes

def calculate_statistics(text_with_styles):
    text_content = ''.join(item['text'] for item in text_with_styles)
    words = text_content.split()
    
    # Calculate statistics
    stats = {
        'created': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'last_saved': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'pages': 1,  # Simple assumption; adjust as needed
        'words': len(words),
        'characters': len(text_content),
        'lines': text_content.count('\n') + 1,
        'paragraphs': text_content.count('\n\n') + 1,
        'characters_with_spaces': len(text_content.replace('\n', ' ')),  # Including spaces
        'version': '16.00'
    }
    return stats

def convert_text_with_styles_to_html(text_with_styles):
    # Calculate statistics
    stats = calculate_statistics(text_with_styles)

    # HTML header with dynamic metadata
    html_content = f"""<!DOCTYPE html>
    <html xmlns:v='urn:schemas-microsoft-com:vml' xmlns:o='urn:schemas-microsoft-com:office:office'
          xmlns:w='urn:schemas-microsoft-com:office:word' xmlns:m='http://schemas.microsoft.com/office/2004/12/omml'
          xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
        <meta charset='UTF-8'>
        <meta http-equiv='Content-Type' content='text/html; charset=unicode'>
        <meta name='ProgId' content='{os.getenv('Name__')}'>
        <meta name='Generator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='Originator' content={os.getenv('Name__')} {os.getenv('version')}'>
        <meta name="author" content="">

        <!--[if gte mso 9]><xml>
        <o:DocumentProperties>
            <o:LastAuthor>{os.getenv('Name__')}</o:LastAuthor>
            <o:Revision>3</o:Revision>
            <o:TotalTime>4</o:TotalTime>
            <o:Created>{stats['created']}</o:Created>
            <o:LastSaved>{stats['last_saved']}</o:LastSaved>
            <o:Pages>{stats['pages']}</o:Pages>
            <o:Words>{stats['words']}</o:Words>
            <o:Characters>{stats['characters']}</o:Characters>
            <o:Lines>{stats['lines']}</o:Lines>
            <o:Paragraphs>{stats['paragraphs']}</o:Paragraphs>
            <o:CharactersWithSpaces>{stats['characters_with_spaces']}</o:CharactersWithSpaces>
            <o:Version>{stats['version']}</o:Version>
        </o:DocumentProperties>
        </xml><![endif]-->
    """

    # Generate CSS and get class mapping
    css, classes = generate_css(text_with_styles)
    html_content += css + "</head><body>"

    # Group spans into paragraphs or headers
    current_paragraph = []
    current_header = []
    is_header = False

    for index, item in enumerate(text_with_styles):
        class_name = classes[(item['font'], item['size'], item['color'], item['flags'], item['alignment'])]

        if item['size'] > 14 and item['flags'] & 2:  # Example heuristic: large and bold
            if current_paragraph:
                html_content += f"<p>{''.join(current_paragraph)}</p>"
                current_paragraph = []
            is_header = True
            current_header.append(f"<span class='{class_name}'>{item['text']}</span>")
        else:
            if is_header:
                html_content += f"<h1>{''.join(current_header)}</h1>"
                current_header = []
                is_header = False
            current_paragraph.append(f"<span class='{class_name}'>{item['text']}</span>")

        # Detect line breaks or paragraph separations
        if item['text'].endswith('\n') or item['text'].strip() == '':
            if current_paragraph:  # Wrap in a paragraph
                html_content += f"<p>{''.join(current_paragraph)}</p>"
                current_paragraph = []

    # Add the last paragraph or header if they exist
    if current_paragraph:
        html_content += f"<p>{''.join(current_paragraph)}</p>"
    if current_header:
        html_content += f"<h1>{''.join(current_header)}</h1>"

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