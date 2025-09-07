#!/usr/bin/env python3
"""
Setup script for Document Intelligence Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="document-intelligence-agent",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sophisticated RAG system for enterprise document analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/document-intelligence-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "document-agent=document_intelligence_agent:main",
        ],
    },
    keywords="rag, document-analysis, ai, nlp, embeddings, vector-search, openai, langchain",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/document-intelligence-agent/issues",
        "Source": "https://github.com/yourusername/document-intelligence-agent",
        "Documentation": "https://github.com/yourusername/document-intelligence-agent#readme",
    },
)
