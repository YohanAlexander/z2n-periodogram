#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt
from click_shell import shell

# Other Libraries
from src import var

# Plotting style
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('axes', labelsize=16)
plt.style.use('ggplot')


def fig(frequencies: np.array, periodogram: np.array) -> None:
    """
    Creates the periodogram plotting figure.

    Parameters
    ----------
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.
    periodogram : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.

    Returns
    -------
    None
    """

    try:

        plt.close()
        plt.ion()
        plt.tight_layout()
        plt.plot(frequencies, periodogram, color='tab:blue',
                label=f"xmin: {var.fmin:.4e}\nxmax: {var.fmax:.4e}\ndelta: {var.delta:.4e}")
        plt.show()

    except Exception as error:
        click.secho(f'{error}', fg='red')


@shell(prompt=click.style('(plt) >>> ', fg='magenta', bold=True), intro=var.__plot__)
def plot() -> None:
    """
    Interactive plotting window of the Z2n Software.
    """


@plot.command()
def style() -> None:
    """
    Change the plotting style.
    """

    try:

        click.secho("This will reset the figure.", fg='yellow')

        st = click.prompt("Which style")

        plt.style.use(st)

        fig(var.frequencies, var.periodogram)

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def peak() -> None:
    """
    Add vertical line to the peak value.
    """

    plt.axvline(var.peak, color='tab:red', label=f"peak: {var.peak:.4e}")


@plot.command()
def band() -> None:
    """
    Add horizontal line to the bandwidth value.
    """

    plt.axhline(var.band, color='tab:gray', label=f"band: {var.band:.4e}")


@plot.command()
def legend() -> None:
    """
    Add legend to the figure.
    """

    plt.legend(loc='best')


@plot.command()
def title() -> None:
    """
    Change the title on the figure.
    """

    t = click.prompt("Which title")

    plt.title(t)


@plot.command()
def xlabel() -> None:
    """
    Change the label on the x axis.
    """

    lab = click.prompt("Which label")

    plt.xlabel(lab)


@plot.command()
def xscale() -> None:
    """
    Change the scale on the x axis.
    """

    scale = click.prompt("Which scale [linear, log, symlog, logit]")

    plt.xscale(scale)


@plot.command()
def xlim() -> None:
    """
    Change the limites on the x axis.
    """

    low = click.prompt("Which lower limit", type=float)

    up = click.prompt("Which upper limit", type=float)

    plt.ylim([low, up])


@plot.command()
def ylabel() -> None:
    """
    Change the label on the y axis.
    """

    lab = click.prompt("Which label")

    plt.ylabel(lab)


@plot.command()
def yscale() -> None:
    """
    Change the scale on the y axis.
    """

    scale = click.prompt("Which scale [linear, log, symlog, logit]")

    plt.xscale(scale)


@plot.command()
def ylim() -> None:
    """
    Change the limites on the y axis.
    """

    low = click.prompt("Which lower limit", type=float)

    up = click.prompt("Which upper limit", type=float)

    plt.ylim([low, up])


def save() -> None:
    """
    Save the plot into a file.
    """

    txt = click.prompt("Name of the output file")

    out = click.prompt("Which format [jpg, png, pdf, ps, eps]")

    if out == 'jpg':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'png':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'pdf':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'ps':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'eps':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    else:
        click.secho(f"{out} format not supported.", fg='red')
