#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt

# Other Libraries
import z2n.stats as stats
import z2n.prompt as prompt
import z2n.globals as glob

# Plotting Style
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('axes', labelsize=16)

# Global Functions


def cli() -> None:
    """Entry point to the Z2n Software."""

    try:

        prompt.z2n()

    except Exception as error:
        click.secho(f'{error}', fg='red')


def plot() -> None:
    """Create the interactive periodogram plotting figure."""

    try:

        plt.close()
        plt.ion()

        if glob.axis == 0:

            glob.figure, glob.axes = plt.subplots(glob.axis + 1)
            glob.axes.plot(glob.frequencies, glob.periodogram,
                           color='tab:blue', label="Z2n Potency")

        else:

            glob.figure, glob.axes = plt.subplots(glob.axis + 1, sharex=True)
            glob.axes[0].plot(glob.frequencies, glob.periodogram, color='tab:blue',
                              label="Z2n Potency")
            glob.axes[1].plot(glob.background, color='tab:cyan',
                              label="Background")

        plt.tight_layout()

    except Exception as error:
        click.secho(f'{error}', fg='red')


def uncertainty() -> None:
    """Estimate uncertainty from regions on the forest of values."""

    try:

        click.secho(
            "Select regions on the plot to estimate error.", fg='yellow')

        regions = click.prompt("How many regions of uncertainty", type=int)

        for region in range(regions):

            means = np.zeros(regions)

            if click.confirm(f"Did you already select the region {region + 1}"):

                ax = plt.gca().get_xlim()

                ax_x = np.where(np.isclose(glob.frequencies, ax[0], 0.1))
                ax_y = np.where(np.isclose(glob.frequencies, ax[1], 0.1))
                lower = np.rint(np.median(ax_x)).astype(int)
                upper = np.rint(np.median(ax_y)).astype(int)

                means[region] = np.mean(glob.periodogram[lower: upper])

        glob.forest = np.mean(means)

        glob.peak = stats.peak(glob.frequencies, glob.periodogram)
        click.echo(click.style("Peak value of the periodogram: ",
                               fg='cyan') + f"{glob.peak} Hz")

        glob.error = 0
        click.echo(click.style("Uncertainty of the system: ",
                               fg='cyan') + f"{glob.error} +/-")

        glob.band = np.max(glob.periodogram) - glob.forest
        click.echo(click.style("Bandwidth of the system: ",
                               fg='cyan') + f"{glob.band} Hz")

        glob.pulsed = stats.pfraction(glob.time, glob.periodogram)
        click.echo(click.style("Pulsed fraction of the peak: ",
                               fg='cyan') + f"{glob.pulsed * 100} %")

    except Exception as error:
        click.secho(f'{error}', fg='red')
        click.secho("Failed to determine uncertainty.", fg='red')


def z2n() -> None:
    """Applies the Z2n statistics and display values to the user."""

    try:

        glob.period = stats.period(glob.time)
        click.echo(click.style(
            "Period of observation on the signal: ", fg='cyan') + f"{glob.period} s")

        glob.frequency = stats.frequency(glob.time)
        click.echo(click.style("Sampling frequency on the signal: ",
                               fg='cyan') + f"{glob.frequency} Hz")

        click.echo(click.style(
            "Minimum frequency used: ", fg='cyan') + f"{glob.fmin} Hz")

        click.echo(click.style(
            "Maximum frequency used: ", fg='cyan') + f"{glob.fmax} Hz")

        click.echo(click.style(
            "Frequency steps used: ", fg='cyan') + f"{glob.delta} Hz")

        glob.frequencies = np.arange(glob.fmin, glob.fmax, glob.delta)

        try:
            glob.periodogram = stats.periodogram(glob.time, glob.frequencies)
            click.secho('Finished to calculate the periodogram.', fg='green')

        except Exception as error:
            click.secho(f'{error}', fg='red')
            click.secho('Failed to calculate the periodogram.', fg='red')
            glob.fits = 0

        else:
            plot()
            uncertainty()
            # gauss()

    except Exception as error:
        click.secho(f'{error}', fg='red')


def gauss() -> None:
    """Adjust a normal distribution to the peak value."""


if __name__ == "__main__":
    cli()
