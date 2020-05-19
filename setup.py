#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name='z2n-periodogram',
        version='1.4.0',
        install_requires=[
            'click',
            'click-shell',
            'matplotlib',
            'astropy',
            'pandas',
            'numpy',
            'numba',
            'tqdm',
            'dask',
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
        author='Yohan Alexander',
        author_email='yohanfranca@gmail.com',
        description='A program for interative periodograms analysis.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/yohanalexander/z2n-periodogram',
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Astronomy",
        ],
        packages=setuptools.find_namespace_packages(),
    )
