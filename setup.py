from setuptools import setup, find_packages

setup(
    name='RahebPDF',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyMuPDF',
        'Pillow',
        'python-dotenv',
        'langdetect',
        'pdf2docx',
        'python-docx',
        'multipledispatch',
    ],
    entry_points={
        'console_scripts': [
            'convert-pdf-to-html=pdf_to_html.utils:convert_pdf_to_html',
        ],
    },
    url='https://github.com/rahebsaeed/RahebPDF',
    author='Raheb Saeed',
    author_email='raheebareef@gmail.com',
    description='A library for converting PDF to HTML and vice versa',
    packages=find_packages(),
)