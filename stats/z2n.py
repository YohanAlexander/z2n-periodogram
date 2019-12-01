#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
from tqdm import trange, tqdm

def period(arrival_times: np.array) -> float:
    """
    Calculates the period of observation on the given time series.

    Parameters
    ----------
    arrival_times : numpy.array
        Numpy array that represents the photon arrival times.

    Returns
    -------
    period : float
        Float number that represents the observation period.
    """

    try:

        first = np.min(arrival_times)

        last = np.max(arrival_times)

        period = last - first

        return period

    except Exception as error:
        click.echo(error)

def frequency(arrival_times: np.array) -> float:
    """
    Calculates sampling rate of the given time series.

    Parameters
    ----------
    arrival_times : numpy.array
        Numpy array that represents the photon arrival times.

    Returns
    -------
    freq : float
        Float number that represents the the nyquist frequency.
    """
    
    try:

        interval = period(arrival_times)

        freq = (1 / interval)

        return freq
    
    except Exception as error:
        click.echo(error)

def phases(arrival_times: np.array, frequencies: np.array) -> np.array:
    """
    Calculates phase values from photon arrival times.

    Parameters
    ----------
    arrival_times : numpy.array
        Numpy array that represents the photon arrival times.
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.

    Returns
    -------
    values : numpy.array
        Numpy array that represents the phase values for each photon.
    """

    try:

        photon = 0
        #derivative = np.gradient(frequencies)
        #derivative2 = np.gradient(derivative)
        values = np.zeros(shape=(arrival_times.size, frequencies.size))
        delta = np.zeros_like(arrival_times)

        delta = arrival_times - arrival_times[0]

        for time in tqdm(delta, desc='Calculating phase values'):
            termo1 = time * frequencies
            #termo2 = (time ** 2) * derivative / 2
            #termo3 = (time ** 3) * derivative2 / 6
            #termo = termo1 + termo2 + termo3
            values[photon] = termo1
            photon += 1

        values = values - np.floor(values)

        return values

    except Exception as error:
        click.echo(error)

def periodogram(phase_values: np.array, frequencies: np.array) -> np.array:
    """
    Applies the Z2n statistics to phase values and normalize.

    Parameters
    ----------
    phase_values : numpy.array
        Numpy array that represents the phase values for each photon.
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.

    Returns
    -------
    values : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.
    """

    try:

        harmonics = 1

        values = np.zeros_like(frequencies)

        pi = np.zeros_like(phase_values)

        pi = 2 * np.pi * phase_values
    
        for freq in trange(frequencies.size, desc='Calculating Z2n Statistics'):
            cos = np.sum(np.cos(harmonics * pi[:,freq])) ** 2
            sin = np.sum(np.sin(harmonics * pi[:,freq])) ** 2
            fft = cos + sin
            values[freq] = fft
        
        values = (2/phase_values.size) * values

        return values

    except Exception as error:
        click.echo(error)

def peak(periodogram: np.ndarray, frequencies: np.ndarray) -> float:
    """
    Gets the value of the natural frequency on the periodogram.

    Parameters
    ----------
    frequencies : numpy.ndarray
        Numpy array that represents the frequency spectrum.
    periodogram : numpy.ndarray
        Numpy array that represents the the power spectrum of each frequency on the spectrum.

    Returns
    -------
    peak : float
        Float number that represents the periodogram peak.
    """

    try:

        index, = np.where(periodogram == np.max(periodogram))

        peak = frequencies[index[0]]

        return peak

    except Exception as error:
        click.echo(error)