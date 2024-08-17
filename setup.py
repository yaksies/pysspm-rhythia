from setuptools import setup, find_packages

setup(
    name="pysspm",  # Replace with your package name
    version="0.1.0",  # Initial release version
    author="David Jedlovsky",
    author_email="Dev.DavidJed@gmail.com",
    description="A Python library dedicated to reading, writing, and modifying the SSPM file format",
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/David-Jed/pysspm",  # Replace with your project'As URL
    packages=find_packages(),  # Automatically finds your package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Adjust based on your needs
    install_requires=[
        "numpy",
    ],
    extras_require={
        "dev": [
            "pytest",  # Add dev dependencies here
        ],
    },
    include_package_data=True,
)
