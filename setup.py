#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import setuptools

# Other Libraries
import z2n.globals as glob

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name='z2n-periodogram',
        version=glob.__version__,
        package_dir={"": "z2n"},
        install_requires=[
            'click',
            'click-shell',
            'matplotlib',
            'astropy',
            'scipy',
            'dask',
            'numpy',
            'numexpr',
            'tqdm'
        ],
        tests_require=['pytest'],
        extras_require={
            "dev": [
                "pytest",
            ],
        },
        entry_points='''
            [console_scripts]
            z2n=z2n.main:cli
        ''',
        author=glob.__author__,
        author_email=glob.__email__,
        description=glob.__description__,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=glob.__url__,
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=setuptools.find_namespace_packages(where="z2n"),
    )
