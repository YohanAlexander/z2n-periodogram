#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other libraries
import click
import numpy as np
from numba import jit
from tqdm import trange
from scipy import optimize
import matplotlib.pyplot as plt


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
    if not series.observation:
        observation(series)
    series.sampling = (1 / series.observation)


@jit(nopython=True, parallel=True, fastmath=True)
def phase(times: np.array, freq: float, harm: int) -> np.array:
    """
    Calculate the phase values.

    Parameters
    ----------
    times : np.array
        An array that represents the times.
    freq : float
        A float that represents the frequency.
    harm : int
        A int that represents the harmonics.

    Returns
    -------
    values : np.array
        An array that represents the phase values.
    """
    values = times * freq
    values = values - np.floor(values)
    values = values * 2 * np.pi * harm
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
    value : float
        A float that represents the square value.
    """
    value = value ** 2
    return value


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
def z2n(times: np.array, freq: float, harm: int) -> float:
    """
    Calculate the Z2n potency value.

    times : np.array
        An array that represents the times.
    freq : float
        A float that represents the frequency.
    harm : int
        A int that represents the harmonics.

    Returns
    -------
    value : float
        A float that represents the Z2n potency.
    """
    phases = phase(times, freq, harm)
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
    for freq in trange(
            series.bins.size, desc=click.style(
                'Calculating the periodogram', fg='yellow')):
        for harmonic in range(series.harmonics):
            series.z2n[freq] = series.z2n[freq] + \
                z2n(series.time, series.bins[freq], harmonic + 1)
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
    if not series.frequency:
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
    if not series.potency:
        potency(series)
    pfrac = (2 * series.potency) / series.time.size
    series.pulsed = pfrac ** 0.5


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
    if not series.potency:
        potency(series)
    if not series.forest:
        forest(series)
    series.bandwidth = series.potency - series.forest


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
    click.secho("Select regions to estimate error.", fg='yellow')
    regions = click.prompt("How many regions", type=int)
    if regions > 0:
        means = np.zeros(regions)
        for region in range(regions):
            flag = True
            while flag:
                if click.confirm(f"Is the region {region + 1} selected"):
                    axis = plt.gca().get_xlim()
                    lower = np.where(np.isclose(series.bins, axis[0], 0.1))
                    upper = np.where(np.isclose(series.bins, axis[1], 0.1))
                    low = np.rint(np.median(lower)).astype(int)
                    up = np.rint(np.median(upper)).astype(int)
                    means[region] = np.mean(series.z2n[low:up])
                    flag = False
        series.forest = np.mean(means)
    else:
        click.secho("No regions to estimate error.", fg='yellow')


def gauss(series) -> None:
    """
    Adjust a gaussian to the natural frequency.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    def gaussian(x, amplitude, mean, sigma):
        return amplitude * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))
    if not series.potency:
        potency(series)
    bins = np.array(series.bins)
    z2n = np.array(series.z2n)
    mean = sum(bins * z2n) / sum(z2n)
    sigma = np.sqrt(sum(z2n * (bins - mean) ** 2) / sum(z2n))
    guess = [series.potency, mean, sigma]
    popt, _ = optimize.curve_fit(gaussian, bins, z2n, guess)
    series.frequency = np.absolute(popt[1])
    series.error = np.absolute(popt[2])
    period(series)
    series.noise = np.absolute(
        (1 / (series.frequency + series.error)) - series.period)
    lower = series.frequency - series.error
    upper = series.frequency + series.error
    low = np.where(np.isclose(bins, lower, 0.1))[0][0]
    up = np.where(np.isclose(bins, upper, 0.1))[0][-1]
    # series.z2n[low:up] = gaussian(bins[low:up], *popt)
    # plt.plot(bins[low:up], gaussian(bins[low:up], *popt), color='red')
    del bins
    del z2n
