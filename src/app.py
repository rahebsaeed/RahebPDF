from spire.pdf.common import *
from spire.pdf import *

# Create an object of the PdfDocument class
doc = PdfDocument()
# Load a PDF document
doc.LoadFromFile(r"C:\wamp64\RahebPDF\test\sample.pdf")

# Set the conversion options
convertOptions = doc.ConvertOptions
convertOptions.SetPdfToHtmlOptions(isEmbedFont=False, isEmbedImage=False, imageQuality=1, isSaveAsSvg=False)

# Save the PDF document to HTML format (without SVG)
doc.SaveToFile(r"C:\wamp64\RahebPDF\src\html_output.html", FileFormat.HTML)
doc.Close()
