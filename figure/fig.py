#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

#plt.style.use('science')

def save_fig(frequencies: np.array, statistics: np.array, name: str) -> None:
    """
    Plots the periodogram and saves into a png file.

    Parameters
    ----------
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.
    statistics : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.
    name : str
        Name of the output file.

    Returns
    -------
    None
    """
    
    try:
        plt.ion()
        plt.tight_layout()
        plt.plot(frequencies, statistics, label="Z2n Statistics")
        plt.legend()
        plt.savefig(f"{name}.png")
        click.echo(f"Image file saved at {name}.png")
        plt.show()

    except Exception as error:
        click.echo(error)
        