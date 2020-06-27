#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name='z2n-periodogram',
        version='1.9.7',
        license='MIT',
        python_requires='>=3.6.9',
        install_requires=[
            'intel-openmp',
            'click',
            'pillow',
            'click-shell',
            'matplotlib',
            'termtables',
            'colorama',
            'astropy',
            'psutil',
            'numpy',
            'numba',
            'icc-rt',
            'scipy',
            'h5py',
            'tqdm',
            'tbb',
        ],
        tests_require=['pytest'],
        extras_require={
            "dev": [
                "pytest",
                "mkdocs",
                "mkautodoc",
                "markdown-katex",
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
        url='https://z2n-periodogram.readthedocs.io',
        project_urls={
            "Documentation": "https://z2n-periodogram.readthedocs.io",
            "Source": "https://github.com/yohanalexander/z2n-periodogram",
        },
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
