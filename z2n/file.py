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


def load_hdf5(series) -> None:
    """
    Open hdf5 file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, path='EVENTS', format='hdf5')
    series.time = table['TIME'].data


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
    table = Table(array, names=('FREQUENCY', 'POTENCY'))
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
    table = Table(array, names=('FREQUENCY', 'POTENCY'))
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
    table = Table(array, names=('FREQUENCY', 'POTENCY'))
    table.write(f'{series.output}.fits', format='fits')


def save_hdf5(series) -> None:
    """
    Save the periodogram to hdf5 file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('FREQUENCY', 'POTENCY'))
    table.write(f'{series.output}.hdf5', path='Z2N',
                format='hdf5', compression=True)


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
    table = Table.read(series.input, names=(
        'FREQUENCY', 'POTENCY'), format='ascii')
    series.bins = table['FREQUENCY'].data
    series.z2n = table['POTENCY'].data


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
    table = Table.read(series.input, names=(
        'FREQUENCY', 'POTENCY'), format='csv')
    series.bins = table['FREQUENCY'].data
    series.z2n = table['POTENCY'].data


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
    table = Table.read(series.input, format='fits')
    series.bins = table['FREQUENCY'].data
    series.z2n = table['POTENCY'].data


def plot_hdf5(series) -> None:
    """
    Open hdf5 file and store periodogram.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    table = Table.read(series.input, path='Z2N', format='hdf5')
    series.bins = table['FREQUENCY'].data
    series.z2n = table['POTENCY'].data
