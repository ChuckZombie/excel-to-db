"""
Script de configuration pour Excel to SQLite Converter
"""
from setuptools import setup, find_packages
from pathlib import Path

# Lire le README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Lire les requirements
requirements = (this_directory / "requirements.txt").read_text(encoding='utf-8').splitlines()

setup(
    name="excel-to-db",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Application CLI pour convertir des fichiers Excel en base de données SQLite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/excel-to-db",
    packages=find_packages(),
    py_modules=['main'],  # Inclure main.py en tant que module
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "e2db=main:app",           # Commande ultra-courte (recommandée)
            "excel2db=main:app",       # Commande courte
            "excel-to-db=main:app",    # Commande complète
        ],
    },
    include_package_data=True,
    keywords="excel sqlite database conversion cli",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/excel-to-db/issues",
        "Source": "https://github.com/yourusername/excel-to-db",
    },
)
