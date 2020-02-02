#! /usr/bin/python
# -*- coding: utf-8 -*-

import globals
import click
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('axes', labelsize=16)
plt.style.use('ggplot')


def save_fig(frequencies: np.array, statistics: np.array, peak: float, name: str) -> None:
    """
    Plots the periodogram and saves into a png file.

    Parameters
    ----------
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.
    statistics : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.
    peak : float
        Float number that represents the peak value of the frequency spectrum.
    name : str
        String that represents the name of the output image file.

    Returns
    -------
    None
    """

    if(name == ""):
        raise FileNotFoundError("''")

    try:

        plt.close()
        plt.ion()
        plt.tight_layout()
        plt.plot(frequencies, statistics, color='tab:blue',
                 label=f"Z2n Statistics\nxmin: {globals.fmin:.4e}\n xmax: {globals.fmax:.4e}\n delta: {globals.delta:.4e}")
        plt.axvline(peak, color='tab:red',
                    label=f"Correct frequency\npeak: {globals.peak:.4e}")
        plt.legend(loc='best')
        plt.savefig(name)
        click.echo(f"Image file saved at {name}.png")
        plt.show()

    except Exception as error:
        click.echo(error)
