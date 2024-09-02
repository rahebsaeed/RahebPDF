from .utils import extract_text_from_pdf, extract_images_from_pdf

def convert_pdf_to_html(pdf_path):
    # Step 1: Extract text and images from the PDF
    text = extract_text_from_pdf(pdf_path)
    images = extract_images_from_pdf(pdf_path)
    
    # Step 2: Construct HTML content
    html_content = "<html><body>"
    html_content += "<pre>{}</pre>".format(text)  # Add extracted text
    
    # Add images (assuming they are saved and accessible via URLs or local paths)
    for image_path in images:
        html_content += '<img src="{}">'.format(image_path)
    
    html_content += "</body></html>"
    return html_content
