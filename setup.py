from setuptools import setup, find_packages

setup(
    name='RahebPDF',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',  # This installs the fitz module
        'Pillow',   # This installs the PIL module
    ],
    url='https://github.com/rahebsaeed/RahebPDF',
    author='Raheb Saeed',
    author_email='raheebareef@gmail.com',
    description='A library for converting PDF to HTML and vice versa',
)
