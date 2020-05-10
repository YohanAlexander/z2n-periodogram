#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import os
import click
from click_shell import shell

# Other Libraries
from z2n import series
from z2n import plot

data = series.Series()
noise = series.Series()
figure = plot.Plot(data, noise)

__z2n__ = '''
        Z2n Software, a program for interactive periodograms analysis.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.
        '''

__plt__ = '''
        Interactive plotting window of the Z2n Software.
        Type "help" for more information.
        '''

# Keep this shell at the top
@shell(prompt=click.style('(plt) >>> ', fg='magenta', bold=True), intro=__plt__)
def plt() -> None:
    """Open the interactive periodogram plotting window."""
    figure.add_lines()


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


@click.version_option(prog_name="Z2n Software", version='1.2.0')
@shell(prompt=click.style('(z2n) >>> ', fg='blue', bold=True), intro=__z2n__)
def z2n():
    """
    This program allows the user to calculate periodograms using the Z2n
    statistics a la Buccheri et al. 1983.

    The standard Z2n statistics calculates the phase of each photon and
    the sinusoidal functions above for each photon. Be advised that this
    is very computationally expensive if the number of photons is high.
    """


@z2n.command()
def shell() -> None:
    """Run shell commands."""
    command = click.prompt("Type the command")
    output = os.popen(command).read()
    click.echo(output)


@z2n.command()
def docs() -> None:
    """Open the documentation on the software."""
    url = "https://z2n-periodogram.readthedocs.io"
    click.launch(url)
    click.echo(f"To read the documentation go to {url}")


@z2n.command()
def plot() -> None:
    """Open the interactive plotting window."""
    if data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
        figure.plot_periodogram()
    else:
        figure.plot_figure()
        plt()


@z2n.command()
def run() -> None:
    """Calculate the periodogram."""
    figure.plot_z2n()


@z2n.command()
def back() -> None:
    """Create subplot of a background file."""
    if data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        figure.plot_background()


@z2n.command()
def save() -> None:
    """Save the periodogram to a file."""
    if data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        data.save_file()
