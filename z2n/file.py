#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
from astropy.table import Table
import numpy as np


def load_ascii(series) -> None:
    """
    Open ascii file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, names=('TIME',), format='ascii')
    series.time = table['TIME'].data


def load_csv(series) -> None:
    """
    Open csv file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, names=('TIME',), format='csv')
    series.time = table['TIME'].data


def load_fits(series) -> None:
    """
    Open fits file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    events = Table.read(series.input, hdu='EVENTS', format='fits')
    series.time = events['TIME'].data


def save_ascii(series) -> None:
    """
    Save the periodogram to ascii file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('Frequency', 'Potency'))
    table.write(f'{series.output}.txt', format='ascii')


def save_csv(series) -> None:
    """
    Save the periodogram to csv file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('Frequency', 'Potency'))
    table.write(f'{series.output}.csv', format='csv')


def save_fits(series) -> None:
    """
    Save the periodogram to fits file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('Frequency', 'Potency'))
    table.write(f'{series.output}.fits', format='fits')


def plot_ascii(series) -> None:
    """
    Open ascii file and store periodogram.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, names=('Frequency', 'Potency'))
    series.bins = table['Frequency'].data
    series.z2n = table['Potency'].data


def plot_csv(series) -> None:
    """
    Open csv file and store periodogram.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, names=('Frequency', 'Potency'))
    series.bins = table['Frequency'].data
    series.z2n = table['Potency'].data


def plot_fits(series) -> None:
    """
    Open fits file and store periodogram.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, names=('Frequency', 'Potency'))
    series.bins = table['Frequency'].data
    series.z2n = table['Potency'].data
