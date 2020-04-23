#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
from src.file import text
from astropy.io import fits, ascii


def load_fits(path: str) -> np.array:
    """
    Open fits file and return time series as a numpy array.

    Parameters
    ----------
    path : str
        String that represents full or relative path to a fits file.

    Returns
    -------
    time_series : numpy.array
        Numpy array that represents the arrival times of each photon.
    """

    try:

        data = fits.open(f'{path}')  # open fits file
        event = data['EVENTS'].data  # acesses event header
        time_series = event['TIME']  # stores time series on numpy array
        data.close()

        return time_series

    except Exception as error:
        click.echo(error)

def save_fits(frequencies: np.array, periodogram: np.array, text: str) -> None:
    """
    Saves the frequency spectrum into an formatted ascii file.

    Parameters
    ----------
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.
    periodogram : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.
    text : str
        A formatted String that represents the name of the output file.

    Returns
    -------
    None
    """

    try:

        text.save_ascii(text)

        file = ascii.read(text)
        file.write(f"{text}.fits")

    except Exception as error:
        click.echo(error)
