import numpy
import setuptools
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name='z2n-periodogram',
        version='0.6.0',
        py_modules=['z2n'],
        install_requires=[
            'Cython',
            'Click',
            'Click-shell',
            'matplotlib',
            'astropy',
            'scipy',
            'numpy',
            'tqdm',
        ],
        tests_require=['pytest'],
        extras_require={
            "dev":[
                "pytest",
            ],
        },
        entry_points='''
        [console_scripts]
        z2n=z2n:main
    ''',
        author="Yohan Alexander",
        author_email="yohanfranca@gmail.com",
        description="A fitting package for Z2n Periodograms from FITS files.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/yohanalexander/z2n-periodogram",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        ext_modules=[
            #cythonize("stats/z2n.pyx"),
        ],
        include_dirs=[numpy.get_include()],
    )
