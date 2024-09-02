from setuptools import setup, find_packages

setup(
    name='RahebPDF',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',
        'Pillow',
        # Add other dependencies here
    ],
    url='https://github.com/rahebsaeed/RahebPDF',
    author='Raheb Saeed',
    author_email='raheebareef@gmail.com.com',
    description='A library for converting PDF to HTML and vice versa',
)
