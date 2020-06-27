#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other libraries
import click
import numpy as np
from numba import jit
from tqdm import trange
from scipy import optimize
from scipy.stats import norm
import matplotlib.pyplot as plt


@jit(forceobj=True, parallel=True, fastmath=True)
def exposure(series) -> None:
    """
    Calculate the period of exposure.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    last = series.time[-1]
    first = series.time[0]
    series.exposure = last - first


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
    series.sampling = (1 / series.exposure)


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
def power(sin: float, cos: float) -> float:
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
    value = power(square(sin), square(cos))
    return value


@jit(nopython=True, parallel=True, fastmath=True)
def normalization(spectrum: np.array, normal: float) -> np.array:
    """
    Calculate the normalization values.

    Parameters
    ----------
    spectrum : np.array
        An array that represents the z2n values.
    normal : float
        A float that represents the normalization.

    Returns
    -------
    values : np.array
        An array that represents the normalized values.
    """
    values = spectrum * normal
    return values


@jit(nopython=True, parallel=True, fastmath=True)
def harmonics(time: np.array, freq: float, harm: int) -> np.array:
    """
    Calculate the Z2n harmonics.

    Parameters
    ----------
    series : Series
        A time series object.
    harm : int
        A int that represents the harmonics.

    Returns
    -------
    None
    """
    values = np.zeros(harm)
    for harmonic in range(harm):
        values[harmonic] = z2n(time, freq, harmonic + 1)
    value = summation(values)
    return value


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
    for freq in trange(series.bins.size, desc=click.style(
            'Calculating the periodogram', fg='yellow')):
        series.z2n[freq] = harmonics(
            series.time, series.bins[freq], series.harmonics)
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
    pfrac = (2 * series.potency) / series.time.size
    series.pulsed = pfrac ** 0.5


@jit(nopython=True, parallel=True, fastmath=True)
def gaussian(x, amplitude, mean, sigma):
    """Returns a Gaussian like function."""
    return amplitude * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))


@jit(forceobj=True, parallel=True, fastmath=True)
def fitcurve(function, bins, powerspec, guess):
    """Fit a input curve function to the data."""
    return optimize.curve_fit(function, bins, powerspec, guess)


@jit(forceobj=True, parallel=True, fastmath=True)
def equal(A, B, tol=1e-05):
    """Compare floating point numbers with tolerance."""
    S = round(1/tol)
    return np.in1d(np.around(A*S).astype(int), np.around(B*S).astype(int))


# @jit(forceobj=True, parallel=True, fastmath=True)
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
    flag = 1
    click.secho(
        "Select the peak region to estimate uncertainty.", fg='yellow')
    while flag:
        if click.confirm("Is the peak region selected", prompt_suffix='? '):
            try:
                axis = plt.gca().get_xlim()
                low = np.where(equal(series.bins, axis[0]))[0][0]
                up = np.where(equal(series.bins, axis[1]))[0][-1]
                mean, sigma = norm.fit(series.bins[low:up])
                potency(series)
                guess = [series.potency, mean, sigma]
                popt, _ = fitcurve(
                    gaussian, series.bins[low:up], series.z2n[low:up], guess)
                series.potency = np.absolute(popt[0])
                series.frequency = np.absolute(popt[1])
                period(series)
                series.errorf = np.absolute(popt[2])
                series.errorp = np.absolute(
                    (1 / (series.frequency + series.errorf)) - series.period)
                pfraction(series)
                series.z2n = gaussian(series.bins[low:up], *popt)
                series.bins = series.bins[low:up]
                flag = 0
            except IndexError:
                click.secho("Error on the selection.", fg='red')
