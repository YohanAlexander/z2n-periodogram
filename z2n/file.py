#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import pandas as pd
from astropy.io import fits
import astropy.io.ascii as txt


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
    data = pd.read_csv(series.input, sep=' ', skiprows=1, header=None)
    series.time = data[0].values


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
    data = pd.read_csv(series.input, sep=',', skiprows=1, header=None)
    series.time = data[0].values


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
    with fits.open(series.input) as data:
        event = data['EVENTS'].data
        series.time = event['TIME']


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
    data = pd.DataFrame()
    data['Frequency'] = series.bins
    data['Potency'] = series.z2n
    data.to_csv(f'{series.output}.txt', sep=' ', index=None)


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
    data = pd.DataFrame()
    data['Frequency'] = series.bins
    data['Potency'] = series.z2n
    data.to_csv(f'{series.output}.csv', sep=',', index=None)


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
    save_ascii(series)
    file = txt.read(f'{series.output}.txt')
    file.write(f"{series.output}.fits")


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
    data = pd.read_csv(series.input, sep=' ', skiprows=1, header=None)
    series.bins = data[0].values
    series.z2n = data[1].values


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
    data = pd.read_csv(series.input, sep=',', skiprows=1, header=None)
    series.bins = data[0].values
    series.z2n = data[1].values


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
    with fits.open(series.input) as data:
        event = data[1].data
        series.bins = event['Frequency']
        series.z2n = event['Potency']
