from setuptools import setup, find_packages

setup(
    name="controme-api-async",
    version="0.1.0",
    author="tuxbox",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuxbox/controme-api-async",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        aiohttp==3.11.11
    ],
)