#! /usr/bin/python
# -*- coding: utf-8 -*-


# Other Libraries
import click
import numpy as np
from astropy.table import Table


def load_file(series) -> int:
    """
    Open file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    flag = 0
    table = Table.read(series.input)
    for column in ['TIME', 'time']:
        try:
            series.time = table[column].data
            series.time = series.time.astype(series.time.dtype.name)
            flag = 0
            break
        except KeyError:
            click.secho(f"Column {column} not found.", fg='red')
            flag = 1
    return flag


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
    series.time = series.time.astype(series.time.dtype.name)


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
    series.time = series.time.astype(series.time.dtype.name)


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
    series.time = series.time.astype(series.time.dtype.name)


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
    series.time = series.time.astype(series.time.dtype.name)


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
    table = Table(array, names=('FREQUENCY', 'POWER'))
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
    table = Table(array, names=('FREQUENCY', 'POWER'))
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
    table = Table(array, names=('FREQUENCY', 'POWER'))
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
    table = Table(array, names=('FREQUENCY', 'POWER'))
    table.write(f'{series.output}.hdf5', format='hdf5', compression=True)
