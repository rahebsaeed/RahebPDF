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

    def save_image(self, image_bytes: bytes, image_number: int, ext) -> str:
        """Save an image to the images directory and return the image path."""
        image_path = os.path.join(self.image_dir, f"image_{image_number}.{ext}")
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        return image_path

    def extract_text_with_styles_and_images(self):
        """Extract styled text and images from the PDF."""
        self.text_with_styles = []  # Clear previous data
        image_number = 0  # Initialize image counter

        try:
            doc = fitz.open(self.pdf_path)
            total_pages = doc.page_count
            print(f"Total pages in PDF: {total_pages}")

            for page_number, page in enumerate(doc):
                print(f"Processing page {page_number + 1} of {total_pages}")

                # Start a new page container in HTML
                page_width, page_height = page.rect.width, page.rect.height
                page_html = (
                    f"<div style='position: relative; width: {page_width}px; height: {page_height}px; border: 1px solid black; margin-bottom: 20px;'>"
                )

                # Extract text
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if block['type'] == 0:  # Text block
                     line_html = f"<p class='paragraph' style='position: absolute;  left: {block['bbox'][0]}px; top: {block['bbox'][1]}px;''>"   
                     for line in block['lines']:
                            # Start a new paragraph for each line
                            
                            for span in line['spans']:
                                # Prepare properties for HTML representation
                                bold = (span['flags'] & 2**4) != 0
                                italic = (span['flags'] & 2**1) != 0
                                monospaced = (span['flags'] & 2**3) != 0
                                serifed = (span['flags'] & 2**2) != 0
                                superscripted = (span['flags'] & 2**0) != 0
                                color = f"#{span['color']:06x}"
                                background_color = span.get('background', 'transparent')
                                styled_text = span['text']

                                # Build the style string
                                style = f"font-size: {span['size']}px; color: {color}; background-color: {background_color}; "
                                if bold:
                                    styled_text = f"<b>{styled_text}</b>"
                                if italic:
                                    styled_text = f"<i>{styled_text}</i>"
                                if monospaced:
                                    style += "font-family: monospace; "
                                elif serifed:
                                    style += "font-family: serif; "
                                else:
                                    style += f"font-family: {span['font']};"
                                if superscripted:
                                    style += "vertical-align: super; font-size: smaller; "

                                # Create span HTML
                                span_html = (
                                    f"<span style='{style} position: relative; left: {span['origin'][0] - span['bbox'][0]}px; top: {span['origin'][1] - span['bbox'][1]}px; right: {span['bbox'][2] - line['bbox'][2]}px; bottom: {span['bbox'][3] - span['bbox'][3]}px;'>"
                                    f"{styled_text}</span>"
                                )

                                # Append the span HTML to the line HTML
                                line_html += span_html

                            
                            # Append the line HTML to the page HTML
                            page_html += line_html
                    # Close the paragraph tag
                    line_html += "</p>"

                # Extract images
                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]  # XREF of the image
                    base_image = doc.extract_image(xref)  # Use extract_image to get image data
                    image_info = page.get_image_info(hashes=False, xrefs=xref)

                    if base_image and image_info:  # Ensure the image was successfully extracted and image_info is available
                        image_info_dict = image_info[0] if isinstance(image_info, list) else image_info

                        image_bytes = base_image["image"]
                        image_format = base_image["ext"]  # Get image format
                        image_path = self.save_image(image_bytes, image_number, image_format)

                        # Update image number after saving
                        image_number += 1

                        bbox = image_info_dict["bbox"]  # Access the bbox from the dictionary
                        x1, y1, x2, y2 = bbox

                        # Create image HTML with absolute positioning
                        image_html = (
                            f"<img src='{image_path}' alt='Image {image_number}' "
                            f"style=\"position: absolute; left: {x1}px; top: {y1}px; width: {base_image['xres']}px; height: {base_image['yres']}px;\" />"
                        )

                        # Append image HTML to the page HTML
                        page_html += image_html

                # Close the page container
                page_html += "</div>"

                # Append the page content to the main text_with_styles list
                self.text_with_styles.append({
                    "type": "page",
                    "text": page_html
                })

            doc.close()

            # Check if any content was extracted
            if not self.text_with_styles:
                print("No content extracted from PDF!")
            else:
                print(f"Content extracted from {total_pages} pages")

            # Save extracted data to a JSON file for verification
            with open(os.path.join(os.path.dirname(self.output_path), "text_with_styles.json"), "w", encoding="utf-8") as f:
                json.dump(self.text_with_styles, f, indent=4)
            print("Text with styles and images saved to text_with_styles.json")

            return self.text_with_styles

        except Exception as e:
            print(f"Error extracting styled text and images: {e}")
