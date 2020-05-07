#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
from tqdm import tqdm


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


def phase(arrival_time: float, frequency: float) -> float:
    """
    Calculate the phase value of the photon arrival time.

    Parameters
    ----------
    arrival_time : float
        Float that represents the photon arrival time.
    frequency : float
        Float that represents the frequency spectrum.

    Returns
    -------
    value : float
        Float that represents the phase value of the photon.
    """

    try:

        value = arrival_time * frequency

        value = value - np.floor(value)

        value = 2 * np.pi * value

        return value

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

        freq = 0

        potency = np.zeros_like(frequencies)

        cossenos = np.zeros_like(arrival_times)

        senos = np.zeros_like(arrival_times)

        z2n = click.style('Calculating the periodogram', fg='yellow')

        for frequency in tqdm(frequencies, desc=z2n):

            time = 0

            for arrival_time in arrival_times:

                value = phase(arrival_time, frequency)
                senos[time] = np.sin(value)
                cossenos[time] = np.cos(value)
                time += 1

            seno = senos.sum() ** 2
            cosseno = cossenos.sum() ** 2
            potency[freq] = seno + cosseno
            freq += 1

        potency = potency * (2 / arrival_times.size)

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
