from setuptools import setup, find_packages

setup(
    name="wer_cer_calculator",
    version="0.1.2",
    description="A package to calculate Word Error Rate (WER) and Character Error Rate (CER) from ground truth and hypothesis data.",
    author="Kritarth",
    author_email="kritarthranjan.iitb@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "jiwer",
    ],
    entry_points={
        "console_scripts": [
            "wer_cer_calculator=wer_cer_calculator.core:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)