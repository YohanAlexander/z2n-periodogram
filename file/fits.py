#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
from astropy.io import fits


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
