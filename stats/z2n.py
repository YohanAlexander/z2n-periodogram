#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import trange, tqdm

def nyquist(arrival_times):
    """
    Calculates sampling rate of the given time series.
    """

    interval = np.mean(np.diff(arrival_times))

    period = arrival_times.size * interval

    freq = 1 / period

    return freq / 2

def phases(arrival_times, frequencies):
    """
    Calculates phase values from photon arrival times.
    """

    photon = 0
    values = np.zeros(shape=(arrival_times.size, frequencies.size))
    delta = np.zeros_like(arrival_times)

    delta = arrival_times - arrival_times[0]

    for time in tqdm(delta):
        p = time * frequencies
        values[photon] = p
        photon += 1

    return values - np.floor(values)

def periodogram(phase_values, frequencies):
    """
    Applies the Z2n statistics to phase values and normalize.
    """

    values = np.zeros_like(frequencies)

    pi = np.zeros_like(phase_values)

    pi = 2 * np.pi * phase_values
    
    for freq in trange(frequencies.size):
        cos = np.sum(np.cos(pi[:,freq])) ** 2
        sin = np.sum(np.sin(pi[:,freq])) ** 2
        fft = cos + sin
        values[freq] = fft

    return 2/phase_values.size * values