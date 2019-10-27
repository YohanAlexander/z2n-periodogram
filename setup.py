import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
    name='z2n-periodogram',
    version='0.1',
    py_modules=['z2n'],
    install_requires=[
        'Click',
        'Click-shell',
    ],
    entry_points='''
        [console_scripts]
        z2n=z2n:main
    ''',
    author="Yohan Alexander",
    author_email="yohanfranca@gmail.com",
    description="A fitting package for Z2n Statistics from FITS files.",
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