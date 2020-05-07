#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import csv
import click
import numpy as np
import pandas as pd
from astropy.io import fits
import astropy.io.ascii as txt


def load_ascii(path: str) -> np.array:
    """
    Open ascii file and return time series as a numpy array.

    Parameters
    ----------
    path : str
        String that represents full or relative path to a fits file.

    Returns
    -------
    time_series : numpy.array
        Array that represents the arrival times of each photon.
    """

    try:

        data = pd.read_csv(f'{path}', sep=' ', header=None)
        time_series = data[0].values

        return time_series

    except Exception as error:
        click.secho(f'{error}', fg='red')


def load_csv(path: str) -> np.array:
    """
    Open csv file and return time series as a numpy array.

    Parameters
    ----------
    path : str
        String that represents full or relative path to a fits file.

    Returns
    -------
    time_series : numpy.array
        Array that represents the arrival times of each photon.
    """

    try:

        data = pd.read_csv(f'{path}', sep=',', header=None)
        time_series = data[0].values

        return time_series

    except Exception as error:
        click.secho(f'{error}', fg='red')


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
        Array that represents the arrival times of each photon.
    """

    try:

        data = fits.open(f'{path}')
        event = data['EVENTS'].data
        time_series = event['TIME']
        data.close()

        return time_series

    except Exception as error:
        click.secho(f'{error}', fg='red')


def save_ascii(frequencies: np.array, periodogram: np.array, text: str) -> None:
    """
    Save the frequency spectrum into an formatted ascii file.

    Parameters
    ----------
    frequencies : numpy.array
        Array that represents the frequency spectrum.
    periodogram : numpy.array
        Array that represents the potency of each frequency on the spectrum.
    text : str
        A formatted string that represents the name of the output file.

    Returns
    -------
    None
    """

    try:

        header = "Frequency Z2n-Potency\n"

        with open(f'{text}.txt', 'w') as file:
            if file.tell() == 0:
                file.write(header)
            for freq, spec in zip(frequencies, periodogram):
                file.write(f"{freq} {spec}\n")

        click.secho(f"Text file saved at {text}.txt", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


def save_csv(frequencies: np.array, periodogram: np.array, text: str) -> None:
    """
    Save the frequency spectrum into an formatted csv file.

    Parameters
    ----------
    frequencies : numpy.array
        Array that represents the frequency spectrum.
    periodogram : numpy.array
        Array that represents the potency of each frequency on the spectrum.
    text : str
        A formatted string that represents the name of the output file.

    Returns
    -------
    None
    """

    try:

        header = ["Frequency", "Z2n-Potency"]

        with open(f'{text}.csv', 'w') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(header)
            for freq, spec in zip(frequencies, periodogram):
                writer.writerow([f"{freq}", f"{spec}"])

        click.secho(f"Csv file saved at {text}.csv", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


def save_fits(frequencies: np.array, periodogram: np.array, text: str) -> None:
    """
    Save the frequency spectrum into an formatted fits file.

    Parameters
    ----------
    frequencies : numpy.array
        Array that represents the frequency spectrum.
    periodogram : numpy.array
        Array that represents the potency of each frequency on the spectrum.
    text : str
        A formatted string that represents the name of the output file.

    Returns
    -------
    None
    """

    try:

        save_ascii(frequencies, periodogram, text)

        file = txt.read(text)
        file.write(f"{text}.fits")

        click.secho(f"Fits file saved at {text}.fits", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')
