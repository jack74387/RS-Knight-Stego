"""
RS-Knight 隱寫系統安裝腳本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rs-knight-stego",
    version="1.0.0",
    author="RS-Knight-Stego Contributors",
    author_email="",
    description="A robust image steganography system with Reed-Solomon error correction and Knight's Tour path selection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/RS-Knight-Stego",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "isort>=5.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rs-knight-stego=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="steganography, image-processing, reed-solomon, error-correction, knight-tour, security",
    project_urls={
        "Bug Reports": "https://github.com/your-username/RS-Knight-Stego/issues",
        "Source": "https://github.com/your-username/RS-Knight-Stego",
        "Documentation": "https://github.com/your-username/RS-Knight-Stego#readme",
    },
)