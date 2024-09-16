from dotenv import load_dotenv
import os
import fitz 
from langdetect import detect, DetectorFactory
from pdf2docx import Converter
import json

# Ensure consistent results
DetectorFactory.seed = 0

load_dotenv()

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()
    
    doc.close()
    return text

def detect_language(text):
    try:
        # Detect language and return language code
        lang_code = detect(text)
        return lang_code
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "unknown"

def get_language_code(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    lang_code = detect_language(text)
    
    # Return the detected language code directly
    return lang_code

#save as files HTML
def save_html(html_content, output_path):
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)




def extract_text_with_styles(pdf_path):
    text_with_styles = []
    doc = fitz.open(pdf_path)
    blocks = []
    tables = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        tables = page.find_tables()
        if tables.tables:
                print(tables[0].extract())
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    line_text = ""
                    for span in line['spans']:
                        # Extract background color; default to transparent if not present
                        background_color = span.get('background', 'transparent')
                        bbox = span.get('bbox', (0, 0, 0, 0))

                        # Detect bold and italic
                        bold = (span['flags'] & 2) != 0
                        italic = (span['flags'] & 1) != 0

                        # Convert integer color to hex format
                        color = f"#{span['color']:06x}"

                        # Append styled text to line_text
                        styled_text = span['text']
                        if bold:
                            styled_text = f"<b>{styled_text}</b>"
                        if italic:
                            styled_text = f"<i>{styled_text}</i>"

                        line_text += f"<span style='font-family: {span['font']}; font-size: {span['size']}px; color: {color}; background-color: {background_color};'>{styled_text}</span>"

                        size = int(span.get('size', 12))  # Default size if not provided
                        text_with_styles.append({
                            "text": line_text,
                            "font": span['font'],
                            "size": size,  
                            "color": span['color'],
                            "background": background_color,
                            "flags": span['flags'],
                            "alignment": block.get('alignment', 0),
                            "bbox": bbox
                        })
    doc.close()

    # Convert data to JSON and save to files
    with open("blocks.json", "w") as f:
        json.dump(blocks, f)
    with open("text_with_styles.json", "w") as f:
        json.dump(text_with_styles, f)


    # Save table data as plain text
    with open("tables.txt", "w") as f:
        for table in tables:
            if isinstance(table, list):
                for row in table:
                    row_str = "\t".join(str(cell) if cell is not None else "" for cell in row)
                    f.write(row_str + "\n")
            f.write("\n")
            
    
    return text_with_styles, blocks


def detect_list_type(line_text):
    # Detects if a line starts with list markers (e.g., bullets, numbers)
    list_markers = {
        'circle': ('●', '○', '◯', '⦿', '◉', '⦾', '◦', '◘'),
        'disc': ('•', '‣', '⁃', '∙', '⁍', '⁌'),
        'square': ('■', '□', '▪', '▫'),
        'number': [str(i) + '.' for i in range(1, 10)],
        'letter': [chr(i) + '.' for i in range(65, 91)],  # A. to Z.
        'latin': [chr(i) + '.' for i in range(97, 123)]  # a. to z.
    }

    for list_type, markers in list_markers.items():
        if any(line_text.strip().startswith(marker) for marker in markers):
            return list_type

    return None


def detect_body_styles(blocks):
    # Initialize margins to a high value to find the minimum margin on the page
    left_margin = float('inf')
    right_margin = float('inf')
    top_margin = float('inf')
    bottom_margin = float('inf')

    # Detect margins based on block positions and page size (assumed A4 for this example)
    for block in blocks:
        if 'bbox' in block:
            bbox = block['bbox']
            left_margin = min(left_margin, bbox[0])
            right_margin = min(right_margin, 595.3 - bbox[2])  # A4 width in points
            top_margin = min(top_margin, bbox[1])
            bottom_margin = min(bottom_margin, 841.9 - bbox[3])  # A4 height in points

    # Convert margins from points to CSS-friendly format (pt)
    margin_left = f"{left_margin * 0.3528}pt"
    margin_right = f"{right_margin * 0.3528}pt"
    margin_top = f"{top_margin * 0.3528}pt"
    margin_bottom = f"{bottom_margin * 0.3528}pt"

    # Set default values for tab interval and word wrap
    tab_interval = '0.5in'
    word_wrap = 'break-word'

    return {
        'margin-left': margin_left,
        'margin-right': margin_right,
        'margin-top': margin_top,
        'margin-bottom': margin_bottom,
        'tab-interval': tab_interval,
        'word-wrap': word_wrap
    }

def generate_css(text_with_styles):
    css = "<style>"
    classes = {}
    class_counter = 0

    for item in text_with_styles:
        style_key = (item['font'], item['size'], item['color'], item['background'], item['flags'], item['alignment'])
        if style_key not in classes:
            class_name = f"text-style-{class_counter}"
            classes[style_key] = class_name
            class_counter += 1

            color = f"#{item['color']:06x}"
            font_weight = "bold" if item['flags'] & 2 else "normal"
            font_style = "italic" if item['flags'] & 1 else "normal"

            align_map = {0: 'left', 1: 'center', 2: 'right', 3: 'justify'}
            text_align = align_map.get(item['alignment'], 'left')

            css += f"""
            .{class_name} {{
                font-family: '{item['font']}';
                font-size: {item['size']}px;
                color: {color};
                background-color: {item['background']};
                font-weight: {font_weight};
                font-style: {font_style};
                text-align: {text_align};
            }}
            """
    
    css += "</style>"
    return css, classes

def generate_body_css(styles):
    # Generate CSS for the body based on detected styles
    body_css = f"""
    <style>
    body {{
        tab-interval: {styles['tab-interval']};
        word-wrap: {styles['word-wrap']};
        margin-left: {styles['margin-left']};
        margin-top: {styles['margin-top']};
        margin-right: {styles['margin-right']};
        margin-bottom: {styles['margin-bottom']};
    }}
    </style>
    """
    return body_css


def convert_text_with_styles_to_html(text_with_styles, blocks, pdf_path):
    # Extract detected body styles
    body_styles = detect_body_styles(blocks)
    body_css = generate_body_css(body_styles)
    lang_code = get_language_code(pdf_path)
    

    html_content = f"""<!DOCTYPE html>
    <html lang="{lang_code}">
    <head>
        <meta http-equiv=Content-Type content="text/html; charset=unicode">
        <meta charset='UTF-8'>
        <meta http-equiv='Content-Type' content='text/html; charset=unicode'>
        <meta name='Generator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='Originator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name="author" content="{os.getenv('Name__')}">
        <meta name="keywords" content="">
        <meta name="description" content="">
        <title></title>
        <meta name=viewport content="width=device-width, initial-scale=1.0">
    """
    css, classes = generate_css(text_with_styles)
    html_content += css + body_css + "</head><body>"

    current_list_type = None
    for item in text_with_styles:
        list_type = detect_list_type(item['text'])
        if list_type:
            if current_list_type != list_type:
                if current_list_type:
                    html_content += f"</ul>"  # Close previous list if any
                current_list_type = list_type
                html_content += f"<ul type={current_list_type} >"

            html_content += f"<li>{item['text']}</li>"
        else:
            if current_list_type:
                html_content += f"</ul>"  # Close the list
                current_list_type = None
            html_content += f"<span>{item['text']}</span>"

    if current_list_type:
        html_content += f"</ul>"  # Close the list if still open

    html_content += "</body></html>"
    return html_content

def convert_pdf_to_html(pdf_path, output_path):
    text_with_styles, blocks = extract_text_with_styles(pdf_path)
    html_content = convert_text_with_styles_to_html(text_with_styles, blocks, pdf_path)
    save_html(html_content, output_path)
