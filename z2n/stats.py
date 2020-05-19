#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other libraries
import numpy as np
from tqdm import tqdm
from numba import jit


def observation(series) -> None:
    """
    Calculate the period of observation.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    last = np.max(series.time)
    first = np.min(series.time)
    series.observation = last - first


def sampling(series) -> None:
    """
    Calculate the sampling rate.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    observation(series)
    series.sampling = (1 / series.observation)


@jit(nopython=True, parallel=True)
def phase(times: np.array, bins: float) -> np.array:
    """
    Calculate the phase values.

    Parameters
    ----------
    times : np.array
        An array that represents the times.
    bins : float
        A float that represents the frequency.

    Returns
    -------
    values : np.array
        An array that represents the phase values.
    """
    delta = times * bins
    frac = delta - np.floor(delta)
    values = frac * 2 * np.pi
    return values


@jit(nopython=True, parallel=True)
def sine(phases: np.array) -> np.array:
    """
    Calculate the sine values.

    Parameters
    ----------
    phases : np.array
        An array that represents the phase values.

    Returns
    -------
    values : np.array
        An array that represents the sine values.
    """
    values = np.sin(phases)
    return values


@jit(nopython=True, parallel=True)
def cosine(phases: np.array) -> np.array:
    """
    Calculate the cosine values.

    Parameters
    ----------
    phases : np.array
        An array that represents the phase values.

    Returns
    -------
    values : np.array
        An array that represents the cosine values.
    """
    values = np.cos(phases)
    return values


@jit(nopython=True, parallel=True)
def summation(phases: np.array) -> float:
    """
    Calculate the summation value.

    Parameters
    ----------
    phases : np.array
        An array that represents the phase values.

    Returns
    -------
    value : float
        A float that represents the summation value.
    """
    value = np.sum(phases)
    return value


@jit(nopython=True)
def square(value: float) -> float:
    """
    Calculate the square values.

    Parameters
    ----------
    value : float
        A float that represents the summation value.

    Returns
    -------
    squared : float
        A float that represents the square value.
    """
    squared = np.square(value)
    return squared


@jit(nopython=True)
def z2n(sin: float, cos: float) -> float:
    """
    Calculate the z2n potency value.

    Parameters
    ----------
    sin : float
        A float that represents the sine value.
    cos : float
        A float that represents the cosine value.

    Returns
    -------
    value : float
        A float that represents the z2n potency.
    """
    value = sin + cos
    return value


@jit(nopython=True, parallel=True)
def normalization(z2n: np.array, norm: float) -> np.array:
    """
    Calculate the normalization values.

    Parameters
    ----------
    z2n : np.array
        An array that represents the z2n values.
    norm : float
        A float that represents the normalization.

    Returns
    -------
    values : np.array
        An array that represents the normalized values.
    """
    values = z2n * norm
    return values


def periodogram(series) -> None:
    """
    Calculate the Z2n statistics.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    freq = 0
    for bins in tqdm(series.bins):
        phases = phase(series.time, bins)
        sin = summation(sine(phases))
        cos = summation(cosine(phases))
        series.z2n[freq] = z2n(square(sin), square(cos))
        freq = freq + 1
    series.z2n = normalization(series.z2n, (2 / series.time.size))


def potency(series) -> None:
    """
    Calculate the natural potency.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    series.potency = np.max(series.z2n)


def frequency(series) -> None:
    """
    Calculate the natural frequency.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    index = np.argmax(series.z2n)
    series.frequency = series.bins[index]


def period(series) -> None:
    """
    Calculate the peak period.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    frequency(series)
    series.period = 1 / series.frequency


def pfraction(series) -> None:
    """
    Calculate the pulsed fraction.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    frequency(series)
    pfrac = (2 * series.potency) / series.time.size
    series.pulsed = pfrac ** 0.5


def forest(series) -> None:
    """
    Calculate the forest potency.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    potency(series)
    index = np.argmax(series.z2n)
    low = np.rint(index - (0.2 * index)).astype(int)
    up = np.rint(index + (0.2 * index)).astype(int)
    series.forest = np.mean([series.z2n[low], series.z2n[up]])


def bandwidth(series) -> None:
    """
    Calculate the bandwidth.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    forest(series)
    series.bandwidth = series.potency - series.forest


def error(series) -> None:
    """
    Calculate the uncertainty of the frequency.
    Parameters
    ----------
    series : Series
        A time series object.
    Returns
    -------
    None
    """
    bandwidth(series)
    intersections = np.where(np.isclose(series.z2n, series.bandwidth, 0.1))
    if intersections[0].size:
        low = series.frequency - series.bins[intersections[0][0]]
        up = series.bins[intersections[0][-1]] - series.frequency
        series.error = np.mean([low, up])
    else:
        series.error = 0
