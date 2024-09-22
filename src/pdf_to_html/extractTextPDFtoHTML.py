import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

load_dotenv()

class ExtractTextPDFtoHTML:
    def __init__(self, pdf_path: str, text_with_styles: list, language_detector):
        """Initialize the ExtractTextPDFtoHTML with paths and styles."""
        self.pdf_path = pdf_path
        self.text_with_styles = text_with_styles  # Store the extracted styles 
        self.language_detector = language_detector  # Store the language detector
 
        
    def extract_text_from_pdf(self) -> str:
        """Extract plain text from the PDF."""
        text = ""
        try:
            doc = fitz.open(self.pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        return text

    def detect_list_type(self, line_text: str):
        """Detect if a line is part of a list and return the list type."""
        list_markers = {
            'circle': ('●', '○', '◯', '⦿', '◉', '⦾', '◦', '◘'),
            'disc': ('•', '‣', '⁃', '∙', '⁍', '⁌'),
            'square': ('■', '□', '▪', '▫'),
            'number': [f"{i}." for i in range(1, 10)],
            'letter': [f"{chr(i)}." for i in range(65, 91)]  # A. to Z.
        }
        for list_type, markers in list_markers.items():
            if any(line_text.strip().startswith(marker) for marker in markers):
                return list_type
        return None

    def generate_css(self) -> str:
        """Generate CSS for the extracted styled text."""
        css = "<style>"
        classes = {}
        class_counter = 0

        for item in self.text_with_styles:
            # Skip items that don't have font-related keys (e.g., images)
            if 'font' not in item or 'size' not in item or 'color' not in item or 'background' not in item or 'flags' not in item:
                continue

            style_key = (item['font'], item['size'], item['color'], item['background'], item['flags'])
            if style_key not in classes:
                class_name = f"text-style-{class_counter}"
                classes[style_key] = class_name
                class_counter += 1

                color = f"#{item['color']:06x}"
                font_weight = "bold" if item['flags'] & 2 else "normal"
                font_style = "italic" if item['flags'] & 1 else "normal"

                css += f"""
                .{class_name} {{
                    font-family: '{item['font']}';
                    font-size: {item['size']}px;
                    color: {color};
                    background-color: {item['background']};
                    font-weight: {font_weight};
                    font-style: {font_style};
                }}
                """
        css += "</style>"
        return css

    def convert_text_with_styles_to_html(self) -> str:
        """Convert extracted text with styles to HTML."""
        # No need to assign styles again, they are already passed in the constructor.
        
        # Detect the language
        text = self.extract_text_from_pdf()
        lang_code = self.language_detector.get_language_code(text)

        # Start constructing the HTML content
        html_content = f"""<!DOCTYPE html>
    <html lang="{lang_code}">
    <head>
        <meta charset='UTF-8'>
        <meta name='Generator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='Originator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='author' content='{os.getenv('Name__')}'>
        <title>PDF to HTML</title>
        <meta name=viewport content="width=device-width, initial-scale=1.0">
    """

        # Generate the CSS and add it to the HTML head
        css = self.generate_css()
        html_content += css + "</head><body>"

        # Handle lists and regular content
        current_list_type = None

        for item in self.text_with_styles:
            # Detect if the current text is part of a list
            list_type = self.detect_list_type(item['text'])
            if list_type:
                if current_list_type != list_type:
                    if current_list_type:
                        html_content += f"</ul>"  # Close the previous list if any
                    current_list_type = list_type
                    html_content += f"<ul type='{current_list_type}'>"

                html_content += f"<li>{item['text']}</li>"
            else:
                if current_list_type:
                    html_content += f"</ul>"  # Close the list
                    current_list_type = None

                # Check if the item contains an image tag and handle accordingly
                if "img src" in item['text']:
                    html_content += f"{item['text']}"
                else:
                    html_content += f"<p>{item['text']}</p>"

        # Close any open list
        if current_list_type:
            html_content += f"</ul>"

        html_content += "</body></html>"
        return html_content
