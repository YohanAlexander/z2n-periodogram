#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import pathlib

# Other Libraries
import click
import numpy as np
from astropy.io import fits
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
    ext = pathlib.Path(series.input).suffix
    if ext in ("", ".txt"):
        flag = load_ascii(series)
    elif ext in (".csv", ".ecsv"):
        flag = load_csv(series)
    elif ext in (".hdf", ".h5", ".hdf5", ".he5"):
        flag = load_hdf5(series)
    else:
        flag = load_fits(series)
    return flag


def load_ascii(series) -> int:
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
    flag = 1
    table = Table.read(series.input, format='ascii')
    try:
        series.time = table['TIME'].data
        series.time = series.time.astype(series.time.dtype.name)
        flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                click.secho(f"Column {column} not found.", fg='red')
                table.pprint()
                column = click.prompt(
                    "Which column name", type=str, prompt_suffix='? ')
                series.time = table[column].data
                series.time = series.time.astype(series.time.dtype.name)
                if click.confirm(f"Use column {column}", prompt_suffix='? '):
                    flag = 0
                else:
                    click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


def load_csv(series) -> int:
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
    flag = 1
    table = Table.read(series.input, format='csv')
    try:
        series.time = table['TIME'].data
        series.time = series.time.astype(series.time.dtype.name)
        flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                click.secho(f"Column {column} not found.", fg='red')
                table.pprint()
                column = click.prompt(
                    "Which column name", type=str, prompt_suffix='? ')
                series.time = table[column].data
                series.time = series.time.astype(series.time.dtype.name)
                if click.confirm(f"Use column {column}", prompt_suffix='? '):
                    flag = 0
                else:
                    click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


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
    flag = 0
    try:
        with fits.open(series.input) as events:
            events.info()
            hdu = click.prompt(
                "Which extension number", type=int, prompt_suffix='? ')
            series.time = events[hdu].data['TIME']
            series.time = series.time.astype(series.time.dtype.name)
            flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                with fits.open(series.input) as events:
                    events.info()
                    click.secho(f"Column {column} not found.", fg='red')
                    hdu = click.prompt(
                        "Which extension number", type=int, prompt_suffix='? ')
                    click.clear()
                    table = Table(events[hdu].data)
                    table.pprint()
                    column = click.prompt(
                        "Which column name", type=str, prompt_suffix='? ')
                    series.time = events[hdu].data[column]
                    series.time = series.time.astype(series.time.dtype.name)
                    if click.confirm(f"Use column {column}", prompt_suffix='? '):
                        flag = 0
                    else:
                        click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


def load_hdf5(series) -> int:
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
    flag = 1
    table = Table.read(series.input, format='hdf5')
    try:
        series.time = table['TIME'].data
        series.time = series.time.astype(series.time.dtype.name)
        flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                click.secho(f"Column {column} not found.", fg='red')
                table.pprint()
                column = click.prompt(
                    "Which column name", type=str, prompt_suffix='? ')
                series.time = table[column].data
                series.time = series.time.astype(series.time.dtype.name)
                if click.confirm(f"Use column {column}", prompt_suffix='? '):
                    flag = 0
                else:
                    click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


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
    table.write(f'{series.output}.hdf5', path='z2n',
                format='hdf5', compression=True)
