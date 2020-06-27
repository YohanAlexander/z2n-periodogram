#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import psutil
import shelve
import pathlib

# Other Libraries
import click
import numpy as np
from click_shell import shell
import matplotlib.pyplot as mplt

# Owned Libraries
from z2n import file
from z2n import stats
from z2n import __docs__
from z2n import __version__

from z2n.plot import Plot
from z2n.series import Series
data = Series()
figure = Plot()

__z2n__ = f'''
        Z2n Software ({__version__}), a python program for periodograms analysis.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.
        '''
__plt__ = f'''
        Interactive plotting window of the Z2n Software ({__version__}).
        Type "help" for more information.
        '''


@click.version_option(prog_name='Z2n Software', version=__version__)
@click.option('--docs', 'docs_', is_flag=True, help='Open the documentation and exit.')
@click.option('--title', 'title_', type=str, help='Title of the image file.')
@click.option(
    '--ylabel', 'ylabel_', type=str, show_default=True,
    help='Y label of the image file.', default='Power')
@click.option(
    '--xlabel', 'xlabel_', type=str, show_default=True,
    help='X label of the image file.', default='Frequency (Hz)')
@click.option(
    '--image', type=click.Choice(['png', 'pdf', 'ps', 'eps']),
    help='Format of the image file.', default='ps', show_default=True)
@click.option(
    '--format', 'format_', type=click.Choice(['ascii', 'csv', 'fits', 'hdf5']),
    help='Format of the output file.', default='fits', show_default=True)
@click.option(
    '--ext', type=int, help='FITS extension number.', default=1, show_default=True)
@click.option(
    '--harm', type=int, help='Number of harmonics.', default=1, show_default=True)
@click.option(
    '--range', 'range_', nargs=3, type=float,
    help='Frequency range <fmin fmax delta> (Hz).')
@click.option('--output', 'output_', type=click.Path(), help='Name of the output file.')
@click.option(
    '--input', 'input_', type=click.Path(exists=True), help='Name of the input file.')
@shell(prompt=click.style('(z2n) >>> ', fg='blue', bold=True), intro=__z2n__)
def z2n(input_, output_, format_, range_, harm, ext,
        image, title_, xlabel_, ylabel_, docs_):
    """
    This program allows the user to calculate periodograms, given a time series,
    using the Z2n statistics a la Buccheri et al. 1983.

    The standard Z2n statistics calculates the phase of each arrival time and
    the corresponding sinusoidal functions for each time. Be advised that this
    is very computationally expensive if the number of frequency bins is high.
    """
    with shelve.open('.z2n') as database:
        if docs_:
            click.launch(__docs__)
            click.echo(f"To read the documentation go to {__docs__}")
            exit()
        if input_:
            if not range_:
                data.set_fmin()
                data.set_fmax()
                data.set_delta()
            else:
                data.fmin = range_[0]
                data.fmax = range_[1]
                data.delta = range_[2]
            data.harmonics = harm
            data.input = input_
            default = "z2n_" + pathlib.Path(data.input).stem
            if output_:
                data.output = output_
            else:
                data.output = default
            data.format = format_
            if not file.load_file(data, ext):
                click.secho('Event file loaded.', fg='green')
                data.set_exposure()
                data.set_sampling()
                data.set_nyquist()
                data.get_time()
                data.get_exposure()
                data.get_sampling()
                data.get_nyquist()
                block = (data.fmax - data.fmin) / np.array(data.delta)
                nbytes = np.array(data.delta).dtype.itemsize * block
                click.secho(
                    f"Computation memory {nbytes* 10e-6:.5f} MB", fg='yellow')
                if nbytes < psutil.virtual_memory()[1]:
                    data.bins = np.arange(data.fmin, data.fmax, data.delta)
                    data.get_bins()
                    data.time = np.array(data.time)
                    data.bins = np.array(data.bins)
                    data.z2n = np.zeros(data.bins.size)
                    stats.periodogram(data)
                    click.secho('Periodogram calculated.', fg='green')
                    click.secho(
                        "Values based on the global maximum.", fg='yellow')
                    data.set_potency()
                    data.set_frequency()
                    data.set_period()
                    data.set_pfraction()
                    data.get_potency()
                    data.get_frequency()
                    data.get_period()
                    data.get_pfraction()
                    flag = 1
                    while flag:
                        if pathlib.Path(f"{data.output}.{data.format}").is_file():
                            click.secho("File already exists.", fg='red')
                            data.output = click.prompt(
                                "Name of the file", default, type=click.Path())
                        else:
                            flag = 0
                    if data.format == 'ascii':
                        file.save_ascii(data)
                    elif data.format == 'csv':
                        file.save_csv(data)
                    elif data.format == 'fits':
                        file.save_fits(data)
                    elif data.format == 'hdf5':
                        file.save_hdf5(data)
                    click.secho(
                        f"File saved at {data.output}.{data.format}", fg='green')
                    flag = 1
                    while flag:
                        if pathlib.Path(f"{data.output}.{image}").is_file():
                            click.secho("Image already exists.", fg='red')
                            data.output = click.prompt(
                                "Name of the image", default, type=click.Path())
                        else:
                            flag = 0
                    mplt.plot(
                        data.bins, data.z2n, label='Z2n Power', linewidth=2)
                    mplt.title(title_)
                    mplt.xlabel(xlabel_)
                    mplt.ylabel(ylabel_)
                    mplt.legend(loc='best')
                    mplt.tight_layout()
                    if image == 'png':
                        mplt.savefig(f'{data.output}.{image}', format=image)
                    elif image == 'pdf':
                        mplt.savefig(f'{data.output}.{image}', format=image)
                    elif image == 'ps':
                        mplt.savefig(f'{data.output}.{image}', format=image)
                    elif image == 'eps':
                        mplt.savefig(f'{data.output}.{image}', format=image)
                    click.secho(
                        f"Image saved at {data.output}.{image}", fg='green')
                else:
                    click.secho("Not enough memory available.", fg='red')
            exit()
        else:
            try:
                figure.data.input = database['input']
            except (KeyError):
                pass
            click.echo(__z2n__)
            figure.plot_periodogram()
            database['input'] = figure.data.input


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
    else:
        figure.plot_figure()
        plt()


@z2n.command()
def run() -> None:
    """Calculate the Z2n Statistics."""
    if not figure.plot_periodogram():
        plt()


@z2n.command()
def log() -> None:
    """Save the fit of a gaussian curve."""
    if figure.data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        figure.data.plot()


@z2n.command()
def save() -> None:
    """Save the periodogram on a file."""
    if figure.data.z2n.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')
    else:
        figure.data.save_file()


@shell(prompt=click.style('(plt) >>> ', fg='magenta', bold=True), intro=__plt__)
def plt() -> None:
    """Open the interactive periodogram plotting window."""


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
    """Save the image on a file."""
    figure.save_image()
