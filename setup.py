from setuptools import setup, find_packages

setup(
    name="comic_spider",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "lxml",
        "selenium",
        "aiohttp",
        "aiofiles",
        "numpy",
        "click"
    ],
    entry_points={
        "console_scripts": [
            "comic-spider = comic_spider.cli:cli"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A comic spider for multiple websites",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/comic_spider",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
