# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


with open("requirements.txt") as f:
    required = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="resume-maker",
    version="0.1.0",
    description="Resume maker from json file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ['resume', 'maker', 'builder', 'cv', 'json'],
    url="https://github.com/MehmetUzel",
    author="Mehmet Uzel",
    author_email="98mehmetuzel@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["resume_maker"],
    include_package_data=True,
    install_requires=required
)