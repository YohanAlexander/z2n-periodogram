#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import trange, tqdm

def period(arrival_times):
    """
    Calculates sampling period of the given time series.
    """

    try:
        interval = np.mean(np.diff(arrival_times))

        period = arrival_times.size * interval

        return period

    except Exception as error:
        print(error)

def frequency(arrival_times):
    """
    Calculates sampling rate of the given time series.
    """
    
    try:
        interval = np.mean(np.diff(arrival_times))

        period = arrival_times.size * interval

        freq = 1 / period

        return freq
    
    except Exception as error:
        print(error)

def phases(arrival_times, frequencies):
    """
    Calculates phase values from photon arrival times.
    """

    try:

        photon = 0
        #derivative = np.gradient(frequencies)
        #derivative2 = np.gradient(derivative)
        values = np.zeros(shape=(arrival_times.size, frequencies.size))
        delta = np.zeros_like(arrival_times)

        delta = arrival_times - arrival_times[0]

        for time in tqdm(delta):
            termo1 = time * frequencies
            #termo2 = (time ** 2) * derivative / 2
            #termo3 = (time ** 3) * derivative2 / 6
            #termo = termo1 + termo2 + termo3
            values[photon] = termo1
            photon += 1

        return values - np.floor(values)

    except Exception as error:
        print(error)

def periodogram(phase_values, frequencies):
    """
    Applies the Z2n statistics to phase values and normalize.
    """

    try:

        harmonics = 1

        values = np.zeros_like(frequencies)

        pi = np.zeros_like(phase_values)

        pi = 2 * np.pi * phase_values
    
        for freq in trange(frequencies.size):
            cos = np.sum(np.cos(harmonics * pi[:,freq])) ** 2
            sin = np.sum(np.sin(harmonics * pi[:,freq])) ** 2
            fft = cos + sin
            values[freq] = fft

        return 2/phase_values.size * values

    except Exception as error:
        print(error)
