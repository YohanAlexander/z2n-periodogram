#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import setuptools

# Other Libraries
import z2n.globals as globals

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name=globals.__name__,
        version=globals.__version__,
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
        author=globals.__author__,
        author_email=globals.__email__,
        description=globals.__description__,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=globals.__url__,
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=setuptools.find_namespace_packages(where="z2n"),
    )
