import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from .extractImages import ExtractImages

load_dotenv()

class ExtractTextPDFtoHTML:
    def __init__(self, pdf_path: str, text_with_styles: list, language_detector, output_path):
        """Initialize the ExtractTextPDFtoHTML with paths and styles."""
        self.pdf_path = pdf_path
        self.output_path = output_path
        self.ExtractImages = ExtractImages(pdf_path, output_path)
        self.ExtractImages.extract_text_with_styles_and_images()
        self.text_with_styles = self.ExtractImages.text_with_styles
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
        lang_code = self.language_detector.get_language_code(" ".join([item['text'] for item in self.text_with_styles if item['type'] == 'text']))

        html_content = f"""<!DOCTYPE html>
    <html lang="{lang_code if lang_code else ''}">
    <head>
        <meta charset='UTF-8'>
        <meta name='Generator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='Originator' content='{os.getenv('Name__')} {os.getenv('version')}'>
        <meta name='author' content='{os.getenv('Name__')}'>
        <title>PDF to HTML</title>
        <meta name=viewport content="width=device-width, initial-scale=1.0">
    """

        css = self.generate_css()
        html_content += css + "</head><body>"

        
        if not self.text_with_styles:
            return html_content + "</body></html>"

        for item in self.text_with_styles:
            if item["type"] == "page":
                # Directly add text to HTML
                html_content += item["text"]
            elif item["type"] == "image":
                # Directly add image HTML
                html_content += item["text"]

        html_content += "</body></html>"
        return html_content
