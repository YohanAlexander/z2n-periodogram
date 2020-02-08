#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
from scipy import signal
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


def periodogram(arrival_times: np.array, frequencies: np.array) -> np.array:
    """
    Applies the Z2n statistics to phase values and normalize.

    Parameters
    ----------
    arrival_times : numpy.array
        Numpy array that represents the photon arrival times.
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.

    Returns
    -------
    potency : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.
    """

    try:

        harmonics = 1

        phase_values = phases(arrival_times, frequencies)

        potency = np.zeros_like(frequencies)

        pi = 2 * np.pi * phase_values

        for freq in trange(frequencies.size, desc='Calculating Z2n Statistics'):
            cos = np.sum(np.cos(harmonics * pi[:, freq])) ** 2
            sin = np.sum(np.sin(harmonics * pi[:, freq])) ** 2
            fft = cos + sin
            potency[freq] = fft

        potency = (2/arrival_times.size) * potency

        return potency

    except Exception as error:
        click.echo(error)


def lightcurve(arrival_times: np.array, frequencies: np.array) -> np.array:
    """
    Calculates the lightcurve of the photons with the phase values.

    Parameters
    ----------
    arrival_times : numpy.array
        Numpy array that represents the photon arrival times.
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.

    Returns
    -------
    curve : numpy.array
        Numpy array that represents the lightcurve of the photons.
    """

    try:

        values = phases(arrival_times, frequencies)

        curve = values.mean(axis=0)

        return curve

    except Exception as error:
        click.echo(error)


def peak(frequencies: np.ndarray, periodogram: np.ndarray) -> float:
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

        index = np.argmax(periodogram)

        peak = frequencies[index]

        return peak

    except Exception as error:
        click.echo(error)


def forest(frequencies: np.ndarray, periodogram: np.ndarray) -> float:
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
    uncertainty : float
        Float number that represents the uncertainty of the system.
    """

    try:

        index = np.argmax(periodogram)

        pot = periodogram[index]

        index2 = int(index - (0.2 * index))

        uncertainty = periodogram[index2]

        return uncertainty

    except Exception as error:
        click.echo(error)


def bandwidth(frequencies: np.ndarray, periodogram: np.ndarray) -> float:
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
    band : float
        Float number that represents the bandwidth of the pulse.
    """

    try:

        index = np.argmax(periodogram)

        pot = periodogram[index]

        uncertainty = forest(frequencies, periodogram)

        band = pot - uncertainty

        return band

    except Exception as error:
        click.echo(error)


def pfraction(arrival_times: np.array, periodogram: np.ndarray) -> float:
    """
    Gets the value of the natural frequency on the periodogram.

    Parameters
    ----------
    arrival_times : numpy.array
        Numpy array that represents the photon arrival times.
    periodogram : numpy.ndarray
        Numpy array that represents the the power spectrum of each frequency on the spectrum.

    Returns
    -------
    pulsed : float
        Float number that represents the pulsed fraction of the peak.
    """

    try:

        peak = np.argmax(periodogram)

        pfrac = (2 * peak) / arrival_times.size

        pulsed = pfrac ** 0.5

        return pulsed

    except Exception as error:
        click.echo(error)
