#!~/anaconda3/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import time, sys, os, functools

# Other Libs
from tqdm import trange, tqdm
from astropy.io import fits
from pprint import pprint
import click, collections
from multiprocessing import Pool, freeze_support, RLock
import matplotlib.pyplot as plt
import pandas as pd

# Wrapping Header
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright 2019, Z2n Periodogram' 
__credits__ = ['Yohan Alexander']
__license__ = 'MPL 2.0'
__version__ = '0.1.0'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Dev'

Scientist = collections.namedtuple('Scientist', ['name', 'field', 'born', 'nobel'])

scientists = (
    Scientist(name='Bohr', field='math', born=1895, nobel=True),
    Scientist(name='Harold', field='physics', born=1755, nobel=True),
    Scientist(name='Finn', field='math', born=1875, nobel=True),
    Scientist(name='Nassim', field='chemestry', born=1825, nobel=False),
    Scientist(name='Klaus', field='astronomy', born=1295, nobel=True),
    Scientist(name='Rutherford', field='computer', born=1855, nobel=True),
    Scientist(name='Ada', field='physics', born=1845, nobel=False),
    Scientist(name='Faraday', field='eletric', born=1995, nobel=False),)

def FFT(iterable):
    return {'name': iterable.name, 'age': 2019 - iterable.born}

@click.command()
#@click.argument('')
@click.option('--file', '-f', help='full or relative path to your fits file')
def main(file):
    """
    A python package for optimized Z2n periodograms from fits datasets

    For more information go to https://z2n-periodogram.github.io
    """

    freeze_support()
    with Pool(initializer=tqdm.set_lock, initargs=(RLock(),)) as pool:
        result = tuple(tqdm(pool.imap(FFT, scientists), total=len(scientists)))

    pprint(result)

    return 0

if __name__ == "__main__":
    main()