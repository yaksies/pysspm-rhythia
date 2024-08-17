from setuptools import setup, find_packages

setup(
    name="pysspm",
    version="0.1.0",  # Initial release version
    author="David Jedlovsky",
    author_email="Dev.DavidJed@gmail.com",
    description="A Python library dedicated to reading, writing, and modifying the Rhythia SSPM file format",
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/David-Jed/pysspm",
    packages=find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    keywords=["Rhythia", "Sound space", "SSPM", "Rhythm game"],
    include_package_data=True,
)
