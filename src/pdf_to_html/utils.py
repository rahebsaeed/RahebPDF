from datetime import datetime
from dotenv import load_dotenv
import os
import fitz 
from langdetect import detect, DetectorFactory

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

def extract_text_with_styles(pdf_path):
    text_with_styles = []
    doc = fitz.open(pdf_path)

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    for span in line['spans']:
                        # Print span to check if background is present
                        #print(span)
                        background_color = span.get('background', None)  # Try getting background color
                        if background_color is None:  # Fallback to transparent if not present
                            background_color = 'transparent'
                        
                        text_with_styles.append({
                            "text": span['text'],
                            "font": span['font'],
                            "size": span['size'],
                            "color": span['color'],
                            "background": background_color,
                            "flags": span['flags'],  # To detect bold, italic
                            "alignment": block.get('alignment', 0)  # Alignment info
                        })
    doc.close()
    return text_with_styles

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

            font_weight = "bold" if item['flags'] & 2 else "normal"
            font_style = "italic" if item['flags'] & 1 else "normal"
            color = f"#{item['color']:06x}"
            background_color = f"#{item['background']:06x}" if item['background'] != 'transparent' else 'transparent'
            align_map = {0: 'left', 1: 'center', 2: 'right', 3: 'justify'}
            text_align = align_map.get(item['alignment'], 'left')

            css += f"""
            .{class_name} {{
                font-family: '{item['font']}';
                font-size: {item['size']}px;
                color: {color};
                background-color: {background_color};
                font-weight: {font_weight};
                font-style: {font_style};
                text-align: {text_align};
            }}
            """
    
    css += "</style>"
    return css, classes

def convert_text_with_styles_to_html(text_with_styles, pdf_path):
    # HTML header with dynamic metadata    
    lang_code = get_language_code(pdf_path)

    html_content = f"""<!DOCTYPE html>
    <html xmlns:v='urn:schemas-microsoft-com:vml' xmlns:o='urn:schemas-microsoft-com:office:office'
          xmlns:w='urn:schemas-microsoft-com:office:word' xmlns:m='http://schemas.microsoft.com/office/2004/12/omml'
          xmlns='http://www.w3.org/TR/REC-html40' lang="{lang_code}">
    <head>
        <meta charset='UTF-8'>
        <meta http-equiv='Content-Type' content='text/html; charset=unicode'>
        <meta name='ProgId' content='{os.getenv('Name__')}'>
        <meta name='Generator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='Originator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name="author" content="{os.getenv('Name__')}">
        <meta name="keywords" content="">
        <meta name="description" content="">
        <title></title>
        <link rel=themeData href="index11_files/themedata.thmx">
        <link rel=colorSchemeMapping href="index11_files/colorschememapping.xml">
        <meta charset=UTF-8>
        <meta name=viewport content="width=device-width, initial-scale=1.0">

    """
    css, classes = generate_css(text_with_styles)
    html_content += css + f"</head><body lang={lang_code} style='tab-interval:.5in;word-wrap:break-word;margin-left: 15.0pt;margin-top:15.0pt;margin-right:15.0pt;margin-bottom:15.0pt'>"

    current_paragraph = []
    current_header = []
    is_header = False

    for index, item in enumerate(text_with_styles):
        class_name = classes[(item['font'], item['size'], item['color'], item['background'], item['flags'], item['alignment'])]

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

        if item['text'].endswith('\n') or item['text'].strip() == '':
            if current_paragraph:
                html_content += f"<p>{''.join(current_paragraph)}</p>"
                current_paragraph = []

    if current_paragraph:
        html_content += f"<p>{''.join(current_paragraph)}</p>"
    if current_header:
        html_content += f"<h1>{''.join(current_header)}</h1>"

    html_content += "</body></html>"
    return html_content

def save_html(html_content, output_path):
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

def convert_pdf_to_html(pdf_path, output_path):
    text_with_styles = extract_text_with_styles(pdf_path)
    html_content = convert_text_with_styles_to_html(text_with_styles, pdf_path)
    save_html(html_content, output_path)
