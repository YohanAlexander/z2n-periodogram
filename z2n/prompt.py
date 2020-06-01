#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
from click_shell import shell

# Owned Libraries
from z2n import __z2n__
from z2n import __plt__
from z2n import __docs__
from z2n import __version__

from z2n.plot import Plot
figure = Plot()


@click.version_option(prog_name='Z2n Software', version=__version__)
@shell(prompt=click.style('(z2n) >>> ', fg='blue', bold=True), intro=__z2n__)
def z2n():
    """
    This program allows the user to calculate periodograms using the Z2n
    statistics a la Buccheri et al. 1983.

    The standard Z2n statistics calculates the phase of each time and
    the corresponding sinusoidal functions. Be advised that this is very
    computationally expensive if the number of frequency bins is high.
    """


@z2n.command()
def docs() -> None:
    """Open the documentation on the software."""
    click.launch(__docs__)
    click.echo(f"To read the documentation go to {__docs__}")


@z2n.command()
def plot() -> None:
    """Open the interactive plotting window."""
    if figure.data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
        if click.confirm("Do you want to plot from a file"):
            if not figure.plot_file():
                plt()
    else:
        figure.plot_figure()
        plt()


@z2n.command()
def run() -> None:
    """Calculate the Z2n Statistics."""
    if not figure.plot_periodogram():
        plt()


@z2n.command()
def save() -> None:
    """Save the periodogram to a file."""
    if figure.data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        figure.data.save_file()


@shell(prompt=click.style('(plt) >>> ', fg='magenta', bold=True), intro=__plt__)
def plt() -> None:
    """Open the interactive periodogram plotting window."""


@plt.command()
def lines() -> None:
    """Change parameter lines on the figure."""
    figure.plot_frequency()
    figure.plot_bandwidth()


@plt.command()
def title() -> None:
    """Change the title on the figure."""
    figure.change_title()


@plt.command()
def xlabel() -> None:
    """Change the label on the x axis."""
    figure.change_xlabel()


@plt.command()
def xscale() -> None:
    """Change the scale on the x axis."""
    figure.change_xscale()


@plt.command()
def xlim() -> None:
    """Change the limites on the x axis."""
    figure.change_xlim()


@plt.command()
def ylabel() -> None:
    """Change the label on the y axis."""
    figure.change_ylabel()


@plt.command()
def yscale() -> None:
    """Change the scale on the y axis."""
    figure.change_yscale()


@plt.command()
def ylim() -> None:
    """Change the limites on the y axis."""
    figure.change_ylim()


@plt.command()
def save() -> None:
    """Save the image to a file."""
    figure.save_image()
