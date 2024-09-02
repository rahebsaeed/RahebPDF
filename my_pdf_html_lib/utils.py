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
