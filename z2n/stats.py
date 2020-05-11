#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import numpy as np
from tqdm import tqdm


def period(series) -> None:
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
    series.period = last - first


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
    period(series)
    series.freq = (1 / series.period)


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
    sin = np.zeros(series.time.size)
    cos = np.zeros(series.time.size)
    for bins in tqdm(series.bins):
        time = 0
        for sample in series.time:
            phase = sample * bins
            phase -= np.floor(phase)
            phase *= 2 * np.pi
            sin[time] = np.sin(phase)
            cos[time] = np.cos(phase)
            time += 1
        series.z2n[freq] = (sin.sum() ** 2) + (cos.sum() ** 2)
        freq += 1
    series.z2n *= (2 / series.time.size)


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
    series.pot = np.max(series.z2n)


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
    series.peak = series.bins[index]


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
    pfrac = (2 * series.peak) / series.time.size
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
    series.band = series.pot - series.forest


def error(series) -> None:
    """
    Calculate the uncertainty.
    Parameters
    ----------
    series : Series
        A time series object.
    Returns
    -------
    None
    """
    bandwidth(series)
    intersections = np.where(np.isclose(series.z2n, series.band, 0.1))
    if intersections[0].size:
        low = series.peak - series.bins[intersections[0][0]]
        up = series.bins[intersections[0][-1]] - series.peak
        series.error = np.mean([low, up])
    else:
        series.error = 0
