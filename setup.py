from setuptools import setup, find_packages

setup(
    name="up-ocr-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
)
