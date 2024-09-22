from .detectLanguage import DetectLanguage
from .extractImages import ExtractImages
from .extractTextPDFtoHTML import ExtractTextPDFtoHTML

# Load environment variables from .env file
class PDFConverter:
    def __init__(self, pdf_path: str, output_path: str):
        """Initialize the PDF converter with paths and settings."""
        self._pdf_path = pdf_path
        self.output_path = output_path
        self.text_with_styles = []
        self.language_detector = DetectLanguage()
        self.ExtractImages = ExtractImages(pdf_path, output_path)
        self.ExtractTextPDFtoHTML = ExtractTextPDFtoHTML(self._pdf_path, self.text_with_styles, self.language_detector)


    def save_html(self, html_content: str):
        """Save HTML content to a file."""
        try:
            with open(self.output_path, "w", encoding="utf-8") as html_file:
                html_file.write(html_content)
        except Exception as e:
            print(f"Error saving HTML: {e}")

    def convert_pdf_to_html(self):
        """Main function to convert PDF to HTML."""
        self.ExtractImages.extract_text_with_styles_and_images()
        self.text_with_styles = self.ExtractImages.text_with_styles  # Assign the extracted styles and images

        # Pass the extracted styles and language detector
        html_content = self.ExtractTextPDFtoHTML.convert_text_with_styles_to_html()
        self.save_html(html_content)
        print("PDF content converted and saved to output.html")
