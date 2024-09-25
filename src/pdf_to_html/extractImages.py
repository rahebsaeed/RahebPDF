import fitz  # PyMuPDF
import json
import os

class ExtractImages:
    def __init__(self, pdf_path: str, output_path: str):
        """Initialize the ExtractImages with paths."""
        self.pdf_path = pdf_path
        self.output_path = output_path

        # Determine the directory for saving images relative to the output HTML
        output_dir = os.path.dirname(output_path)
        self.image_dir = os.path.join(output_dir, "images")
        os.makedirs(self.image_dir, exist_ok=True)  # Create the images directory if it doesn't exist

        self.text_with_styles = []

    def save_image(self, image_bytes: bytes, image_number: int) -> str:
        """Save an image to the images directory and return the image path."""
        image_path = os.path.join(self.image_dir, f"image_{image_number}.png")
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        return image_path

    def extract_text_with_styles_and_images(self):
        """Extract styled text and images from the PDF."""
        self.text_with_styles = []  # Clear previous data
        image_number = 0  # Initialize image counter

        try:
            doc = fitz.open(self.pdf_path)
            for page_number, page in enumerate(doc):
                # Extract text
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if block['type'] == 0:  # Text block
                        for line in block['lines']:
                            for span in line['spans']:
                                # Prepare properties for HTML representation
                                bold = (span['flags'] & 2) != 0
                                italic = (span['flags'] & 1) != 0
                                color = f"#{span['color']:06x}"
                                background_color = span.get('background', 'transparent')
                                styled_text = span['text']
                                
                                # Apply bold and italic formatting
                                if bold:
                                    styled_text = f"<b>{styled_text}</b>"
                                if italic:
                                    styled_text = f"<i>{styled_text}</i>"

                                # Create span HTML
                                span_html = (
                                    f"<span style='font-family: {span['font']}; font-size: {span['size']}px; "
                                    f"color: {color}; background-color: {background_color}; "
                                    f"position: absolute; left: {span['origin'][0]}px; top: {span['origin'][1]}px;'>"
                                    f"{styled_text}</span>"
                                )
                                
                                # Append the span HTML to the list
                                self.text_with_styles.append({
                                    "type": "text",
                                    "text": span_html
                                })

                # Extract images
                images = page.get_images(page_number, full=True)
                for img in images:
                    xref = img[0]  # XREF of the image
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_path = self.save_image(image_bytes, image_number)
                    image_number += 1
                    
                    # Create image HTML
                    image_html = (
                        f"<img src='{image_path}' alt='Image {image_number}' "
                        f"style='position: absolute; left: {img[1]}px; top: {img[2]}px; width: {img[3]}px; height: {img[4]}px;' />"
                    )
                    
                    # Append image tag to HTML
                    self.text_with_styles.append({
                        "type": "image",
                        "text": image_html
                    })

            doc.close()

            # Check if any content was extracted
            if not self.text_with_styles:
                print("No content extracted from PDF!")
            # Save extracted data to a JSON file for verification
            with open(os.path.join(os.path.dirname(self.output_path), "text_with_styles.json"), "w", encoding="utf-8") as f:
                json.dump(self.text_with_styles, f, indent=4)
            print("Text with styles and images saved to text_with_styles.json")
            return self.text_with_styles

        except Exception as e:
            print(f"Error extracting styled text and images: {e}")