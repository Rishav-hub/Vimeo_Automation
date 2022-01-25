from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="src",
    version="0.0.1",
    author="Bappy Ahmed",
    description="A small package for dvc dl pipeline demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rishav-hub/Vimeo_Automation",
    author_email="entbappy73@gmail.com",
    packages=["src"],
    python_requires=">=3.7",
    install_requires=[]
    
)