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

#@np.vectorize
def phases(arrival_times, frequencies):
    """
    Calculate phase values from arrival times
    """
    photon = 0
    #derivative = np.gradient(frequencies)
    #derivative2 = np.gradient(derivative)
    values = np.zeros(shape=(arrival_times.size, frequencies.size))
    delta = np.zeros_like(arrival_times)

    delta = arrival_times - arrival_times[0]

    for time in delta:
        p1 = time * frequencies
        #p2 = (time ** 2) * derivative / 2
        #p3 = (time ** 3) * derivative2 / 6
        #p = p1 + p2 + p3
        values[photon] = p1
        photon += 1

    return values - np.floor(values)

#@np.vectorize
def periodogram(phase_values, frequencies):
    """
    Transforms values to fourier domain and normalize
    """
    values = np.zeros_like(frequencies)

    pi = np.zeros_like(phase_values)

    pi = 2 * np.pi * phase_values
    
    for freq in range(frequencies.size):
        cos = np.sum(np.cos(pi[:,freq])) ** 2
        sin = np.sum(np.sin(pi[:,freq])) ** 2
        fft = cos + sin
        values[freq] = fft

    return 2/phase_values.size * values

@click.command()
@click.argument('file', type=click.Path())
def z2n(file):
    """
    A python package for optimized Z2n periodograms from fits datasets

    For more information go to https://z2n-periodogram.github.io
    """

    data = fits.open('%s' %file)
    event = data[1].data
    time = event.field(0)
    data.close()

    frequencies = np.arange(1e-4, 1.5e-3, 1e-6)

    click.echo("\nTempo de chegada dos fótons\n")
    click.echo(time)
    out = phases(time, frequencies)
    click.echo("\nValores de fase\n")
    click.echo(out)
    click.echo("\nTransformada para o domínio de Fourier\n")
    out2 = periodogram(out, frequencies)
    click.echo(out2)

    #Parallel
    #freeze_support()
    #with Pool(initializer=tqdm.set_lock, initargs=(RLock(),)) as pool:
    #    result = tuple(tqdm(pool.imap(func, object), total=len(object)))

    plt.plot(frequencies, out2)
    plt.title('Periodograma Z2n')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Amplitude')
    plt.savefig("z2n.png")
    click.echo("\nArquivo salvo em z2n.png\n")

    return 0

if __name__ == "__main__":
    z2n()