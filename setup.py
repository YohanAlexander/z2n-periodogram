import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name='z2n-periodogram',
        version='0.6.0',
        py_modules=['z2n'],
        package_dir={'': 'src'},
        install_requires=[
            'Click',
            'Click-shell',
            'matplotlib',
            'astropy',
            'numpy',
            'numexpr',
            'tqdm'
        ],
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
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
