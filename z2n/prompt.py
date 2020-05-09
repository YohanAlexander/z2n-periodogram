#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import os
import click
from click_shell import shell

# Other Libraries
from z2n import series
from z2n import graph

data = series.Series()
noise = series.Series()
figure = graph.Graph(data, noise)

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


@plt.command()
def peak() -> None:
    """Add vertical line to the natural frequency."""
    if figure.plots == 1:
        figure.axes.axvline(data.peak, color='tab:red')
    else:
        figure.axes[0].axvline(data.peak, color='tab:red')
    click.secho("Peak line added.", fg='green')


@plt.command()
def band() -> None:
    """Add horizontal line to the bandwidth."""
    if figure.plots == 1:
        figure.axes.axhline(data.band, color='tab:gray')
    else:
        figure.axes[0].axhline(data.band, color='tab:gray')
    click.secho("Bandwidth line added.", fg='green')


@plt.command()
def title() -> None:
    """Change the title on the figure."""
    if figure.plots != 1:
        pass
    else:
        figure.axes.set_title(click.prompt("Which title"))
        click.secho("Changed title.", fg='green')


@plt.command()
def xlabel() -> None:
    """Change the label on the x axis."""
    if figure.plots != 1:
        pass
    else:
        figure.axes.set_xlabel(click.prompt("Which label"))
        click.secho("Changed X axis label.", fg='green')


@plt.command()
def xscale() -> None:
    """Change the scale on the x axis."""
    if figure.plots != 1:
        pass
    else:
        figure.axes.set_xscale(click.prompt(
            "Which scale [linear, log, symlog, logit]"))
        click.secho(f"Changed X axis scale.", fg='green')


@plt.command()
def xlim() -> None:
    """Change the limites on the x axis."""
    if figure.plots != 1:
        pass
    else:
        low = click.prompt("Which lower limit", type=float)
        up = click.prompt("Which upper limit", type=float)
        figure.axes.set_xlim([low, up])
        click.secho(f"Changed X axis limits.", fg='green')


@plt.command()
def ylabel() -> None:
    """Change the label on the y axis."""
    if figure.plots != 1:
        pass
    else:
        figure.axes.set_ylabel(click.prompt("Which label"))
        click.secho("Changed y axis label.", fg='green')


@plt.command()
def yscale() -> None:
    """Change the scale on the y axis."""
    if figure.plots != 1:
        pass
    else:
        figure.axes.set_yscale(click.prompt(
            "Which scale [linear, log, symlog, logit]"))
        click.secho(f"Changed y axis scale.", fg='green')


@plt.command()
def ylim() -> None:
    """Change the limites on the y axis."""
    if figure.plots != 1:
        pass
    else:
        low = click.prompt("Which lower limit", type=float)
        up = click.prompt("Which upper limit", type=float)
        figure.axes.set_ylim([low, up])
        click.secho(f"Changed y axis limits.", fg='green')


@plt.command()
def save() -> None:
    """Save the image to a file."""
    if not figure.save_image():
        click.secho(f"Saved at {figure.output}.{figure.format}", fg='green')
    else:
        click.secho(f"{figure.format} format not supported.", fg='red')


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
    click.launch('https://z2n-periodogram.readthedocs.io')
    click.echo(
        "To read the documentation go to https://z2n-periodogram.readthedocs.io")


@z2n.command()
def plot() -> None:
    """Open the interactive plotting window."""
    if data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
        if click.confirm("Do you want to plot from a file"):
            if not data.get_z2n():
                click.secho("File loaded.", fg='green')
            else:
                click.secho(f"{data.format} format not supported.", fg='red')
    else:
        if not figure.plot_figure():
            plt()
        else:
            click.secho("Error ploting the figure.", fg='red')


@z2n.command()
def run() -> None:
    """Calculate the periodogram."""
    if data.input != "":
        if click.confirm("Do you want to use another file"):
            if not data.load_file():
                click.secho("File loaded.", fg='green')
                if not data.set_z2n():
                    click.secho(
                        "Select regions to estimate error.", fg='yellow')
                    figure.change_forest()
                    data.get_parameters()
            else:
                click.secho(f"{data.format} format not supported.", fg='red')
        else:
            click.secho("This will recalculate the periodogram.", fg='yellow')
            if click.confirm("Recalculate with different limits"):
                figure.recalculate_figure()
    else:
        if not data.load_file():
            click.secho("File loaded.", fg='green')
            if not data.set_z2n():
                click.secho("Select regions to estimate error.", fg='yellow')
                figure.change_forest()
                data.get_parameters()
        else:
            click.secho(f"{data.format} format not supported.", fg='red')


@z2n.command()
def back() -> None:
    """Create subplot of a background file."""
    if data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        if figure.plots == 2:
            opt = click.prompt("Change the background [1] or remove it [2]")
            if opt == '1':
                noise.load_file()
                noise.bins = data.bins
                noise.set_periodogram()
                figure.add_background()
            elif opt == '2':
                figure.rm_background()
                click.secho("Background file removed.", fg='green')
            else:
                click.secho("Select '1' or '2'.", fg='red')
        else:
            noise.load_file()
            noise.bins = data.bins
            noise.set_periodogram()
            figure.add_background()


@z2n.command()
def save() -> None:
    """Save the periodogram to a file."""
    if data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        if not data.save_file():
            click.secho(f"Saved at {data.output}.{data.format}", fg='green')
        else:
            click.secho(f"{data.format} format not supported.", fg='red')
