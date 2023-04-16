from setuptools import setup, find_packages

setup(
    name="upstage",
    version="0.2.0-rc1",
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
