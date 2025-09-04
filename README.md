# RahebPDF

RahebPDF is a lightweight Python toolkit for extracting content from PDF files and converting PDFs to clean, semantic HTML. It supports text extraction (with style metadata), image extraction, simple table detection, and language detection. It is designed for automation, research, and content republishing workflows.

Key goals:
- Reliable extraction of text and images
- Produce readable HTML suitable for further processing
- Small, dependency-light codebase with a simple CLI and importable API

## Features

- PDF → HTML conversion
- Text extraction with basic style metadata
- Image extraction to separate files
- Basic table detection and CSV/table exports
- Language detection utilities
- Command-line interface for batch processing

## Installation

From PyPI (recommended, if published)
```powershell
pip install RahebPDF
```

From source (Windows)
```powershell
git clone https://github.com/rahebsaeed/RahebPDF.git
cd RahebPDF
pip install -e .
```

Create and activate a virtual environment (recommended)
```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

## Quickstart

CLI
```powershell
# Convert a PDF to HTML
python -m pdf_to_html.cli convert input.pdf output.html

# Extract images from a PDF to ./images/
python -m pdf_to_html.cli extract-images input.pdf ./images
```

Python API
```python
from pdf_to_html.utils import convert_pdf_to_html

convert_pdf_to_html("input.pdf", "output.html")
```

Adjust imports if you installed in editable mode or are running from the repo root.

## Project structure

A typical repository layout:

```
RahebPDF/
│
├── src/
│   └── pdf_to_html/
│       ├── __init__.py
│       ├── detectLanguage.py
│       ├── extractImages.py
│       ├── extractTextPDFtoHTML.py
│       ├── tables.py
│       ├── utils.py
│       └── __pycache__/
│
├── test/
│   ├── app.py
│   ├── arabic.pdf
│   ├── blocks.json
│   ├── doc.html
│   ├── fonts.json
│   ├── img_.json
│   ├── output.csv
│   ├── output.html
│   ├── resarch.pdf
│   ├── sample.pdf
│   ├── tables.json
│   ├── tables.txt
│   ├── test.ram
│   ├── text_with_styles.json
│   ├── Wiki_Test_Image.jpg
│   └── images/
│       ├── image_0.jpeg
│       ├── image_1.jpeg
│       └── ...
│
├── setup.py
├── requirements.txt
├── .env
├── .pypirc
├── license
├── EADME.md
└── command.txt
```


## Usage notes

- Output HTML is intentionally simple and semantic to make downstream processing easier.
- Large PDFs may require increased memory; process large files in chunks where possible.
- For best OCR/text extraction on scanned PDFs, run an OCR step (e.g., Tesseract) before using RahebPDF.

## Development

Run tests (from repo root on Windows):
```powershell
pip install -r requirements-dev.txt
pytest
```

Linting and formatting:
```powershell
pip install black flake8
black .
flake8 .
```

## Contributing

Contributions are welcome. Please:
- Open an issue to discuss larger changes
- Fork the repo, create a feature branch, and submit a PR
- Include tests for new functionality and keep changes minimal and focused

## License

See the license file in the repository (LICENSE). If none present, assume MIT-style permissive license unless otherwise stated.

## Contact

Author: Raheb Saeed
Email: raheebareef@gmail.com