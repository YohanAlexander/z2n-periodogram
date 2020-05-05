#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import numexpr as ne
from tqdm import trange, tqdm


def period(arrival_times: np.array) -> float:
    """
    Calculate the period of observation on the given time series.

    Parameters
    ----------
    arrival_times : numpy.array
        Array that represents the photon arrival times.

    Returns
    -------
    periodo : float
        Float number that represents the observation period.
    """

    try:

        first = np.min(arrival_times)

        last = np.max(arrival_times)

        periodo = last - first

        return periodo

    except Exception as error:
        click.secho(f'{error}', fg='red')


def frequency(arrival_times: np.array) -> float:
    """
    Calculate the sampling rate of the given time series.

    Parameters
    ----------
    arrival_times : numpy.array
        Array that represents the photon arrival times.

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
        click.secho(f'{error}', fg='red')


def phases(arrival_times: np.array, frequencies: np.array) -> np.array:
    """
    Calculate the phase values of the photon arrival times.

    Parameters
    ----------
    arrival_times : numpy.array
        Array that represents the photon arrival times.
    frequencies : numpy.array
        Array that represents the frequency spectrum.

    Returns
    -------
    values : numpy.array
        Array that represents the phase values for each photon.
    """

    try:

        photon = 0

        values = np.zeros(shape=(arrival_times.size, frequencies.size))

        start = np.min(arrival_times)

        delta = ne.evaluate('arrival_times - start')

        desc = click.style('Calculating phase values', fg='yellow')

        for time in tqdm(delta, desc=desc):
            values[photon] = ne.evaluate('time * frequencies')
            photon += 1

        frac = np.floor(values)

        values = ne.evaluate('values - frac')

        return values

    except Exception as error:
        click.secho(f'{error}', fg='red')


def periodogram(arrival_times: np.array, frequencies: np.array) -> np.array:
    """
    Apply the Z2n statistics to the phase values and normalize.

    Parameters
    ----------
    arrival_times : numpy.array
        Array that represents the photon arrival times.
    frequencies : numpy.array
        Array that represents the frequency spectrum.

    Returns
    -------
    potency : numpy.array
        Array that represents the potency of each frequency on the spectrum.
    """

    try:

        harmonics = 1

        phase_values = phases(arrival_times, frequencies)

        potency = np.zeros_like(frequencies)

        pie = np.pi

        pulse = ne.evaluate('2 * pie * phase_values')

        desc = click.style('Calculating Z2n Statistics', fg='yellow')

        for freq in trange(frequencies.size, desc=desc):
            cosseno = np.sum(np.cos(harmonics * pulse[:, freq])) ** 2
            seno = np.sum(np.sin(harmonics * pulse[:, freq])) ** 2
            fft = ne.evaluate('cosseno + seno')
            potency[freq] = fft

        norm = (2 / arrival_times.size)

        potency = ne.evaluate('norm * potency')

        return potency

    except Exception as error:
        click.secho(f'{error}', fg='red')


def peak(frequencies: np.array, statistics: np.array) -> float:
    """
    Get the value of the natural frequency on the periodogram.

    Parameters
    ----------
    frequencies : numpy.array
        Array that represents the frequency spectrum.
    periodogram : numpy.array
        Array that represents the the potency of each frequency on the spectrum.

    Returns
    -------
    peak_value : float
        Float number that represents the periodogram peak.
    """

    try:

        index = np.argmax(statistics)

        peak_value = frequencies[index]

        return peak_value

    except Exception as error:
        click.secho(f'{error}', fg='red')


def pfraction(arrival_times: np.array, statistics: np.array) -> float:
    """
    Get the pulsed fraction of the natural frequency on the periodogram.

    Parameters
    ----------
    arrival_times : numpy.array
        Array that represents the photon arrival times.
    periodogram : numpy.array
        Array that represents the the potency of each frequency on the spectrum.

    Returns
    -------
    pulsed : float
        Float number that represents the pulsed fraction of the peak.
    """

    try:

        peak_value = np.argmax(statistics)

        pfrac = (2 * peak_value) / arrival_times.size

        pulsed = pfrac ** 0.5

        return pulsed

    except Exception as error:
        click.secho(f'{error}', fg='red')
