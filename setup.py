#!/usr/bin/env python3

from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="pynav2",
        version="2.0",
        packages=find_packages(),
        # metadata for upload to PyPI
        author="sloft",
        author_email="nomail@example.com",
        description="Headless programmatic web browser on top of Requests and Beautiful Soup",
        license="GNU Lesser General Public License Version 3 (LGPLv3)",
        keywords=["programmatic", "web", "browser"],
        url="https://github.com/sloft/pynav2/",
        download_url="https://pypi.org/project/pynav/#files",
        python_requires='>=3.4',
        install_requires=[
            'requests',
            'beautifulsoup4',
      ],
        classifiers = [
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
	"Operating System :: OS Independent",
	"License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
	"Development Status :: 4 - Beta",
	"Environment :: Console",
	"Topic :: Internet",
	"Intended Audience :: Developers",
	"Topic :: Internet :: WWW/HTTP",
	"Topic :: Internet :: WWW/HTTP :: Browsers",
	"Topic :: Internet :: WWW/HTTP :: Indexing/Search",
	"Topic :: Internet :: WWW/HTTP :: Site Management",
	"Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
	"Topic :: Software Development :: Libraries",
	"Topic :: Software Development :: Libraries :: Python Modules",
	],
        long_description = long_description,
        long_description_content_type='text/markdown'
)
