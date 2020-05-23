#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other libraries
import numpy as np
from tqdm import tqdm
from numba import jit


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(nopython=True, parallel=True, fastmath=True)
def phase(times: np.array, freq: float) -> np.array:
    """
    Calculate the phase values.

    Parameters
    ----------
    times : np.array
        An array that represents the times.
    freq : float
        A float that represents the frequency.

    Returns
    -------
    values : np.array
        An array that represents the phase values.
    """
    delta = times * freq
    frac = delta - np.floor(delta)
    values = frac * 2 * np.pi
    return values


@jit(nopython=True, parallel=True, fastmath=True)
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


@jit(nopython=True, parallel=True, fastmath=True)
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


@jit(nopython=True, parallel=True, fastmath=True)
def summation(values: np.array) -> float:
    """
    Calculate the summation value.

    Parameters
    ----------
    values : np.array
        An array that represents the phase values.

    Returns
    -------
    value : float
        A float that represents the summation value.
    """
    value = np.sum(values)
    return value


@jit(nopython=True, parallel=False, fastmath=True)
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
    squared = value ** 2
    return squared


@jit(nopython=True, parallel=False, fastmath=True)
def spectrum(sin: float, cos: float) -> float:
    """
    Calculate the Z2n potency value.

    Parameters
    ----------
    sin : float
        A float that represents the sine value.
    cos : float
        A float that represents the cosine value.

    Returns
    -------
    value : float
        A float that represents the Z2n potency.
    """
    value = sin + cos
    return value


@jit(nopython=True, parallel=False, fastmath=True)
def z2n(times: np.array, freq: float) -> float:
    """
    Calculate the Z2n potency value.

    times : np.array
        An array that represents the times.
    freq : float
        A float that represents the frequency.

    Returns
    -------
    value : float
        A float that represents the Z2n potency.
    """
    phases = phase(times, freq)
    sin = summation(sine(phases))
    cos = summation(cosine(phases))
    value = spectrum(square(sin), square(cos))
    return value


@jit(nopython=True, parallel=True, fastmath=True)
def normalization(spec: np.array, norm: float) -> np.array:
    """
    Calculate the normalization values.

    Parameters
    ----------
    spec : np.array
        An array that represents the z2n values.
    norm : float
        A float that represents the normalization.

    Returns
    -------
    values : np.array
        An array that represents the normalized values.
    """
    values = spec * norm
    return values


@jit(forceobj=True, parallel=True, fastmath=True)
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
    for freq in tqdm(range(series.bins.size)):
        series.z2n[freq] = z2n(series.time, series.bins[freq])
    series.z2n = normalization(series.z2n, (2 / series.time.size))


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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


@jit(forceobj=True, parallel=True, fastmath=True)
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
