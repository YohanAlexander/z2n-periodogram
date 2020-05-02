#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import setuptools

# Other Libraries
from src import var

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name=var.__name__,
        version=var.__version__,
        py_modules=['z2n'],
        install_requires=[
            'click',
            'click-shell',
            'matplotlib',
            'astropy',
            'scipy',
            'numpy',
            'numexpr',
            'tqdm'
        ],
        entry_points='''
            [console_scripts]
            z2n=z2n:main
        ''',
        author=var.__author__,
        author_email=var.__email__,
        description=var.__description__,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=var.__url__,
        packages=setuptools.find_packages(),
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
