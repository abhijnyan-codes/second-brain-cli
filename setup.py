from setuptools import setup, find_packages

setup(
    name="second-brain-cli",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
    "typer",
    "rich",
    "rapidfuzz",
    "pyperclip",
    "requests",
],
    entry_points={
        "console_scripts": [
            "brain=brain.cli:app",
        ],
    },
)