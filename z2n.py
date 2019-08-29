#!~/anaconda3/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import time, sys, os, functools, click

# Other Libs
from astropy.io import fits
from tqdm import trange, tqdm
from multiprocessing import Pool, freeze_support, RLock
import matplotlib.pyplot as plt
import plotly as py
import numpy as np

# Wrapping Header
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright 2019, Z2n Periodogram' 
__credits__ = ['Yohan Alexander']
__license__ = 'MPL 2.0'
__version__ = '0.1.0'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Dev'

# Function definitions
#@np.vectorize breaks the code

def phases(arrival_times, frequencies):
    """
    Calculate phase values from arrival times
    """
    photon = 0
    derivative = np.gradient(frequencies)
    derivative2 = np.gradient(derivative)
    values = np.zeros_like(arrival_times)

    for time in arrival_times:
        partial1 = time * frequencies
        partial2 = (time ** 2) * derivative / 2
        partial3 = (time ** 3) * derivative2 / 6
        csum1 = partial1.sum()
        csum2 = partial2.sum()
        csum3 = partial3.sum()
        csum = csum1 + csum2 + csum3
        values[photon] = csum
        photon += 1

    return values - np.floor(values)

def periodogram(phase_values, frequencies):
    """
    Transforms values to fourier domain and normalize
    """
    freq = 0
    values = np.zeros_like(frequencies)

    fft = np.sum(np.cos(phase_values)) ** 2 + np.sum(np.sin(phase_values)) ** 2
    for frequency in frequencies:
        values[freq] = fft

    return (2/len(phase_values)) * values

@click.command()
@click.argument('file', type=click.Path())
@click.option('--fig', '-f', default='fase', type=str, help='Name of the output file')
@click.option('--freq', '-hz', type=float, help='Range of frequencies to analyse')
def z2n(file, fig, freq):
    """
    A python package for optimized Z2n periodograms from fits datasets

    For more information go to https://z2n-periodogram.github.io
    """

    data = fits.open('%s' %file)
    event = data[1].data
    time = event.field(0)
    data.close()

    frequencies = np.arange(0.0001, 0.0015, 0.000001)

    click.echo("\nTempo de chegada dos fótons\n")
    click.echo(time)
    out = phases(time, frequencies)
    click.echo("\nValores de fase\n")
    click.echo(out)
    click.echo("\nTransformada de Fourier\n")
    out2 = periodogram(out, frequencies)
    click.echo(out2)

    #Parallel
    #freeze_support()
    #with Pool(initializer=tqdm.set_lock, initargs=(RLock(),)) as pool:
    #    result = tuple(tqdm(pool.imap(func, object), total=len(object)))

    plt.xlim(0.0001, 0.0015)
    plt.plot(out2)
    plt.title('Periodograma Z2n')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Amplitude')
    plt.savefig("%s.png" %fig)
    click.echo("\nArquivo salvo em %s.png\n" %fig)

    return 0

if __name__ == "__main__":
    z2n()