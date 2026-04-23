from setuptools import setup, find_packages

setup(
    name="second-brain-cli",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "brain=brain.cli:app",
        ],
    },
)