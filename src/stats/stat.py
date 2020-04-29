#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np
import numexpr as ne
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

        start = np.min(arrival_times)

        delta = ne.evaluate('arrival_times - start')

        for time in tqdm(delta, desc='Calculating phase values'):
            termo1 = ne.evaluate('time * frequencies')
            #termo2 = (time ** 2) * derivative / 2
            #termo3 = (time ** 3) * derivative2 / 6
            #termo = termo1 + termo2 + termo3
            values[photon] = termo1
            photon += 1

        frac = np.floor(values)

        values = ne.evaluate('values - frac')

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

        pie = np.pi

        pulse = ne.evaluate('2 * pie * phase_values')

        for freq in trange(frequencies.size, desc='Calculating Z2n Statistics'):
            cosseno = np.sum(np.cos(harmonics * pulse[:, freq])) ** 2
            seno = np.sum(np.sin(harmonics * pulse[:, freq])) ** 2
            fft = ne.evaluate('cosseno + seno')
            potency[freq] = fft

        norm = (2 / arrival_times.size)

        potency = ne.evaluate('norm * potency')

        return potency

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
