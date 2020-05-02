#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt
from click_shell import shell

# Other Libraries
from src import var
from src import stats
from src import file
from src import fig


@click.version_option(prog_name="Z2n Software", version=var.__version__)
@shell(prompt=click.style('(z2n) >>> ', fg='blue', bold=True), intro=var.__intro__)
def cli():
    """
    A python package for optimized Z2n periodograms from fits datasets.

    This program allows the user to calculate periodograms using the Z2n
    statistics a la Buccheri et al. 1983.

    The standard Z2n statistics calculates the phase of each photon and
    the sinusoidal functions above for each photon. Be advised that this
    is very computationally expensive if the number of photons is high.

    The program accepts fits files (.fits) and it is assumed that the
    file contains a header with the event or time series data.
    """


@cli.command()
def docs() -> None:
    """
    Open the documentation on the software.
    """

    try:

        click.launch(var.__docs__)

    except Exception as error:
        click.secho(f'{error}', fg='red')

    click.echo(f"To read the documentation go to {var.__docs__}")


def prompt() -> None:
    """
    Applies the Z2n statistics and display values to the user.
    """

    try:

        var.period = stats.period(var.time)
        click.secho(f"Period of observation on the signal: ", fg='cyan')
        click.echo(f"{var.period} s")

        var.frequency = stats.frequency(var.time)
        click.secho(f"Sampling frequency on the signal: ", fg='cyan')
        click.echo(f"{var.frequency} Hz")

        click.secho(f"Minimum frequency used on the periodogram: ", fg='cyan')
        click.echo(f"{var.fmin} Hz")

        click.secho(f"Maximum frequency used on the periodogram: ", fg='cyan')
        click.echo(f"{var.fmax} Hz")

        click.secho(f"Frequency steps used on the periodogram: ", fg='cyan')
        click.echo(f"{var.delta} Hz")

        var.frequencies = np.arange(var.fmin, var.fmax, var.delta)

        var.periodogram = stats.periodogram(var.time, var.frequencies)

    except Exception as error:
        click.secho(f'{error}', fg='red')


def forest() -> None:
    """
    Calculate the value of uncertainty from regions of the forest.
    """

    # TODO remover media

    click.secho("Select regions on the plot to estimate error.", fg='yellow')

    regions = click.prompt("How many regions of uncertainty", type=int)

    for k in range(regions):

        means = np.zeros(regions)

        if(click.confirm(f"Did you already select the region {k+1}")):

            axes = plt.gca().get_xlim()

            i = np.argwhere(np.isclose(var.frequencies, axes[0], 0.1))
            j = np.argwhere(np.isclose(var.frequencies, axes[1], 0.1))
            l = int(np.rint(np.median(i)))
            u = int(np.rint(np.median(j)))

            means[k] = np.mean(var.periodogram[l: u])

    var.forest = np.mean(means)


def gauss() -> None:
    """
    Adjust the gaussian to the peak and display values to the user.
    """

    # TODO GAUSSIANA

    try:

        forest()

        var.peak = stats.peak(var.frequencies, var.periodogram)
        click.secho(f"Peak value of the periodogram: ", fg='cyan')
        click.echo(f"{var.peak} Hz")

        click.secho(f"Uncertainty of the system: ", fg='cyan')
        click.echo(f"{var.forest} +/-")

        var.band = np.max(var.periodogram) - var.forest
        click.secho(f"Bandwidth of the system: ", fg='cyan')
        click.echo(f"{var.band} Hz")

        var.pulsed = stats.pfraction(var.time, var.periodogram)
        click.secho(f"Pulsed fraction of the peak: ", fg='cyan')
        click.echo(f"{var.pulsed*100} %")

    except Exception as error:
        click.secho(f'{error}', fg='red')


def data() -> None:
    """
    Open fits file and stores photon arrival times.
    """

    path = click.prompt("Path to fits file")

    var.time = file.load_fits(path)

    try:

        if var.time.size != 0:
            click.secho("Fits file loaded correctly.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


def rate() -> None:
    """
    Defines the limits and steps of the periodogram.
    """

    var.fmin = click.prompt("Minimum frequency", type=float)

    var.fmax = click.prompt("Maximum frequency", type=float)

    var.delta = click.prompt("Frequency steps", type=float)


@cli.command()
def plot() -> None:
    """
    Open the interactive plotting window.
    """

    if var.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        fig.fig(var.frequencies, var.periodogram)

        fig.plot()


@cli.command()
def run() -> None:
    """
    Calculate the Z2n periodogram.
    """

    try:

        data()

        if(click.confirm("Do you want to run with the default values")):

            oversample = click.prompt("Frequency steps (delta)", type=float)

            var.frequency = stats.frequency(var.time)
            var.fmin = var.frequency * 2
            var.fmax = var.frequency * 100
            var.delta = oversample

        else:
            rate()

        prompt()

        fig.fig(var.frequencies, var.periodogram)

        gauss()

        fig.plot()

    except Exception as error:
        click.secho(f'{error}', fg='red')


@cli.command()
def save() -> None:
    """
    Save the periodogram into a file.
    """

    if var.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        txt = click.prompt("Name of the output file")

        out = click.prompt("Which format [ascii, fits]")

        if out == 'ascii':
            file.save_ascii(var.frequencies, var.periodogram, txt)

        elif out == 'fits':
            file.save_fits(txt)

        else:
            click.secho(f"{out} format not supported.", fg='red')


@cli.command()
def axis() -> None:
    """
    Change the axis used on the periodogram.
    """

    if var.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        click.secho("This will recalculate the periodogram.", fg='yellow')

        opt = click.prompt("Recalculate the whole periodogram [1] or just a region [2]")

        if opt == '1':

            if(click.confirm("Did you already select the new limits")):

                axes = plt.gca().get_xlim()

                var.fmin = axes[0]
                var.fmax = axes[1]
                var.delta = click.prompt("Frequency steps (delta)", type=float)
                var.frequencies = np.arange(var.fmin, var.fmax, var.delta)

                prompt()

                fig.fig(var.frequencies, var.periodogram)

                gauss()

                fig.plot()

        elif opt == '2':

            if(click.confirm("Did you already select the region")):

                axes = plt.gca().get_xlim()

                i = np.argwhere(np.isclose(var.frequencies, axes[0], 0.1))
                j = np.argwhere(np.isclose(var.frequencies, axes[1], 0.1))
                l = int(np.rint(np.median(i)))
                u = int(np.rint(np.median(j)))
                size = u - l

                fmin = axes[0]
                fmax = axes[1]
                delta = click.prompt("Frequency steps (delta)", type=float)
                freq = np.arange(fmin, fmax, delta)
                period = stats.periodogram(var.time, freq)

                t = (var.frequencies.size - size) + freq.size
                p = l + freq.size

                tempx = np.zeros(t)
                tempy = np.zeros(t)

                tempx[:l] = var.frequencies[:l]
                tempy[:l] = var.periodogram[:l]
                tempx[l:p] = freq
                tempy[l:p] = period
                tempx[p:] = var.frequencies[u:]
                tempy[p:] = var.periodogram[u:]

                var.frequencies = tempx
                var.periodogram = tempy

                fig.fig(var.frequencies, var.periodogram)

                gauss()

                fig.plot()

        else:
            click.secho(f"Select '1' or '2'.", fg='red')


@cli.command()
def back() -> None:
    """
    Create subplot of a background file.
    """

    if var.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        path = click.prompt("Path to background file")

        var.background = file.load_fits(path)

        try:

            if var.background.size != 0:
                click.secho("Background file loaded correctly.", fg='green')

            fig.fig(var.frequencies, var.periodogram)

            figure, axes = plt.subplots(2, sharex=True)
            axes[1].plot(var.background)
            axes[0].plot(var.frequencies, var.periodogram, color='tab:blue',
                    label=f"xmin: {var.fmin:.4e}\nxmax: {var.fmax:.4e}\ndelta: {var.delta:.4e}")

        except Exception as error:
            click.secho(f'{error}', fg='red')
