#!/usr/bin/env python3
"""
Setup script for Biomimetic Bone Scaffold Generator
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="biomimetic-bone-scaffold-voronoi",
    version="2.0.0",
    author="Siqi (Qizaifadacai)",
    author_email="fortyseven0629@gmail.com",
    description="Interactive tool for generating biomimetic bone scaffolds with gradient porous structures using 3D Voronoi tessellation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi",
    project_urls={
        "Bug Tracker": "https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi/issues",
        "Documentation": "https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi#readme",
        "Source Code": "https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "scaffold-generator=新版本演示:main",
        ],
    },
    keywords=[
        "biomimetic",
        "bone scaffold",
        "tissue engineering",
        "voronoi tessellation",
        "3D printing",
        "porous structure",
        "gradient material",
        "stem cell research",
    ],
    include_package_data=True,
    zip_safe=False,
)
