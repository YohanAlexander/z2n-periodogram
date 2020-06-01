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
    events = Table.read(series.input, format='fits')
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
    table = Table.read(series.input, format='hdf5')
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
    def pad(array, size):
        if array.size < size:
            array = np.hstack([array, np.zeros(size)])
        return array
    size = np.absolute(series.time.size - series.bins.size)
    time = pad(series.time, size)
    bins = pad(series.bins, size)
    z2n = pad(series.z2n, size)
    array = np.column_stack((time, bins, z2n))
    table = Table(array, names=('TIME', 'FREQUENCY', 'POTENCY'))
    table.write(f'{series.output}.txt', format='ascii')
    del time
    del bins
    del z2n


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
    def pad(array, size):
        if array.size < size:
            array = np.hstack([array, np.zeros(size)])
        return array
    size = np.absolute(series.time.size - series.bins.size)
    time = pad(series.time, size)
    bins = pad(series.bins, size)
    z2n = pad(series.z2n, size)
    array = np.column_stack((time, bins, z2n))
    table = Table(array, names=('TIME', 'FREQUENCY', 'POTENCY'))
    table.write(f'{series.output}.csv', format='csv')
    del time
    del bins
    del z2n


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
    def pad(array, size):
        if array.size < size:
            array = np.hstack([array, np.zeros(size)])
        return array
    size = np.absolute(series.time.size - series.bins.size)
    time = pad(series.time, size)
    bins = pad(series.bins, size)
    z2n = pad(series.z2n, size)
    array = np.column_stack((time, bins, z2n))
    table = Table(array, names=('TIME', 'FREQUENCY', 'POTENCY'))
    table.write(f'{series.output}.fits', format='fits')
    del time
    del bins
    del z2n


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
    def pad(array, size):
        if array.size < size:
            array = np.hstack([array, np.zeros(size)])
        return array
    size = np.absolute(series.time.size - series.bins.size)
    time = pad(series.time, size)
    bins = pad(series.bins, size)
    z2n = pad(series.z2n, size)
    array = np.column_stack((time, bins, z2n))
    table = Table(array, names=('TIME', 'FREQUENCY', 'POTENCY'))
    table.write(f'{series.output}.hdf5', format='hdf5', compression=True)
    del time
    del bins
    del z2n


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
        'TIME', 'FREQUENCY', 'POTENCY'), format='ascii')
    series.time = np.trim_zeros(table['TIME'].data)
    series.bins = np.trim_zeros(table['FREQUENCY'].data)
    series.z2n = np.trim_zeros(table['POTENCY'].data)


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
        'TIME', 'FREQUENCY', 'POTENCY'), format='csv')
    series.time = np.trim_zeros(table['TIME'].data)
    series.bins = np.trim_zeros(table['FREQUENCY'].data)
    series.z2n = np.trim_zeros(table['POTENCY'].data)


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
    series.time = np.trim_zeros(table['TIME'].data)
    series.bins = np.trim_zeros(table['FREQUENCY'].data)
    series.z2n = np.trim_zeros(table['POTENCY'].data)


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
    table = Table.read(series.input, format='hdf5')
    series.time = np.trim_zeros(table['TIME'].data)
    series.bins = np.trim_zeros(table['FREQUENCY'].data)
    series.z2n = np.trim_zeros(table['POTENCY'].data)
