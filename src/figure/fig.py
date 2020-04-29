#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
import matplotlib.pyplot as plt
from src.cli import globals

# Plotting style

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('axes', labelsize=16)
plt.style.use('ggplot')


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
        plt.plot(frequencies, statistics, color='tab:blue', label=f"xmin: {globals.fmin:.4e}\n xmax: {globals.fmax:.4e}\n delta: {globals.delta:.4e}")
        plt.savefig(name)
        click.echo(f"Image file saved at {name}.png")
        plt.show()

    except Exception as error:
        click.echo(error)
