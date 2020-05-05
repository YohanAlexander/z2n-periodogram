#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt
from click_shell import shell

# Other Libraries
import z2n.stats as stats

# Plotting style
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('axes', labelsize=16)

# Wrapping Header
__version__ = '1.0.0'
__name__ = 'z2n-periodogram'
__author__ = 'Yohan Alexander'
__license__ = 'MIT LICENSE'
__copyright__ = 'Copyright (C) 2020, Z2n Software, by Yohan Alexander.'
__description__ = 'A program for interative periodograms analysis.'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'
__docs__ = 'https://z2n-periodogram.readthedocs.io'
__url__ = 'https://github.com/yohanalexander/z2n-periodogram'
__credits__ = '''
        The Z2n Software was developed by Yohan Alexander as a research project,
        funded by the CNPq Institution, and it is a Open Source initiative.
        '''
__intro__ = f'''
        Z2n Software ({__version__}), a program for interactive periodograms.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.
        '''
__plot__ = '''
        Interactive plotting window of the Z2n Software.
        Type "help" for more information.
        '''

# Global Variables
axis = 0
fits = 0
band = 0
peak = 0
fmin = 0
fmax = 0
delta = 0
error = 0
forest = 0
period = 0
pulsed = 0
frequency = 0
time = np.array([])
periodogram = np.array([])
frequencies = np.array([])
background = np.array([])
figure, axes = plt.subplots()


# Global Functions
def plot() -> None:
    """
    Create the interactive periodogram plotting figure.
    """

    global figure, axes, axis, frequencies, periodogram, background

    try:

        plt.close()
        plt.ion()

        if(axis == 0):

            figure, axes = plt.subplots(axis + 1)
            axes.plot(frequencies, periodogram, color='tab:blue',
                      label=f"Z2n Potency")

        else:

            figure, axes = plt.subplots(axis + 1, sharex=True)
            axes[0].plot(frequencies, periodogram, color='tab:blue',
                         label=f"Z2n Potency")
            axes[1].plot(background, color='tab:cyan',
                         label=f"Background")

        plt.tight_layout()

    except Exception as error:
        click.secho(f'{error}', fg='red')


def forest() -> None:
    """
    Estimate uncertainty from regions on the forest of values.
    """

    global forest, peak, error, band, pulsed, frequencies, periodogram

    try:

        click.secho(
            "Select regions on the plot to estimate error.", fg='yellow')

        regions = click.prompt("How many regions of uncertainty", type=int)

        for k in range(regions):

            means = np.zeros(regions)

            if(click.confirm(f"Did you already select the region {k+1}")):

                ax = plt.gca().get_xlim()

                i = np.where(np.isclose(frequencies, ax[0], 0.1))
                j = np.where(np.isclose(frequencies, ax[1], 0.1))
                l = np.rint(np.median(i)).astype(int)
                u = np.rint(np.median(j)).astype(int)

                means[k] = np.mean(periodogram[l: u])

        forest = np.mean(means)

        peak = stats.peak(frequencies, periodogram)
        click.echo(click.style(f"Peak value of the periodogram: ",
                               fg='cyan') + f"{peak} Hz")

        error = 0
        click.echo(click.style(f"Uncertainty of the system: ",
                               fg='cyan') + f"{error} +/-")

        band = np.max(periodogram) - forest
        click.echo(click.style(f"Bandwidth of the system: ",
                               fg='cyan') + f"{band} Hz")

        pulsed = stats.pfraction(time, periodogram)
        click.echo(click.style(f"Pulsed fraction of the peak: ",
                               fg='cyan') + f"{pulsed*100} %")

    except Exception as error:
        click.secho("Failed to determine uncertainty.", fg='red')


def z2n() -> None:
    """
    Applies the Z2n statistics and display values to the user.
    """

    global time, fits, period, frequency, fmin, fmax, delta, frequencies, periodogram

    try:

        period = stats.period(time)
        click.echo(click.style(
            f"Period of observation on the signal: ", fg='cyan') + f"{period} s")

        frequency = stats.frequency(time)
        click.echo(click.style(f"Sampling frequency on the signal: ",
                               fg='cyan') + f"{frequency} Hz")

        click.echo(click.style(
            f"Minimum frequency used on the periodogram: ", fg='cyan') + f"{fmin} Hz")

        click.echo(click.style(
            f"Maximum frequency used on the periodogram: ", fg='cyan') + f"{fmax} Hz")

        click.echo(click.style(
            f"Frequency steps used on the periodogram: ", fg='cyan') + f"{delta} Hz")

        frequencies = np.arange(fmin, fmax, delta)

        try:
            periodogram = stats.periodogram(time, frequencies)
            click.secho(f'Finished to calculate the periodogram.', fg='green')

        except:
            click.secho(f'Failed to calculate the periodogram.', fg='red')
            fits = 0

        else:
            plot()
            forest()
            # gauss()

    except Exception as error:
        click.secho(f'{error}', fg='red')


# TODO
def gauss() -> None:
    """
    Adjust a normal distribution to the peak value.
    """
