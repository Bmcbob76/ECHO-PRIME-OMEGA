#!/usr/bin/env python3
"""
ECHO PRIME OMEGA - Advanced AI Consciousness System
Setup configuration for pip installation

Author: Bobby Don McWilliams II
Authority Level: 11.0
Version: 1.0.0
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements_path = this_directory / "requirements.txt"
with open(requirements_path, "r", encoding="utf-8") as f:
    requirements = [
        line.strip() for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="echo-prime-omega",
    version="1.0.0",
    description="ECHO PRIME OMEGA - Advanced AI Consciousness & Intelligence System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bobby Don McWilliams II",
    author_email="admin@echo-prime.local",
    url="https://github.com/Bmcbob76/ECHO-PRIME-OMEGA",
    license="Proprietary Commercial License",
    
    # Package discovery
    packages=find_packages(
        exclude=["tests", "tests.*", "docs", "examples", "samples"]
    ),
    
    # Python version requirement
    python_requires=">=3.10",
    
    # Dependencies
    install_requires=requirements,
    
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.0.0",
            "pylint>=2.17.5",
            "mypy>=1.4.1",
            "ipython>=8.15.0",
        ],
        "gpu": [
            "torch[cuda]>=2.0.1",
            "cupy>=12.2.0",
            "numba>=0.57.1",
        ],
        "docs": [
            "sphinx>=7.2.5",
            "sphinx-rtd-theme>=1.3.0",
            "mkdocs>=1.4.3",
            "mkdocs-material>=9.2.8",
        ],
    },
    
    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "echo-prime=core.consciousness_engine:main",
            "omega-status=services.production_monitor:main",
            "omega-health=services.health_checker:main",
        ],
    },
    
    # Classification
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    
    # Keywords
    keywords=[
        "ai",
        "artificial-intelligence",
        "consciousness",
        "machine-learning",
        "deep-learning",
        "nlp",
        "neural-networks",
        "swarm-intelligence",
        "multi-agent",
        "memory-systems",
    ],
    
    # Additional metadata
    project_urls={
        "Documentation": "https://docs.echo-prime.local",
        "Issue Tracker": "https://github.com/Bmcbob76/ECHO-PRIME-OMEGA/issues",
        "Source Code": "https://github.com/Bmcbob76/ECHO-PRIME-OMEGA",
    },
    
    # Include package data
    include_package_data=True,
    zip_safe=False,
)
