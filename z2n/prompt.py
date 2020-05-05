#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt
from click_shell import shell

# Other Libraries
import z2n.globals as globals
import z2n.stats as stats
import z2n.file as file
import z2n.plot as cli


@click.version_option(prog_name="Z2n Software", version=globals.__version__)
@shell(prompt=click.style('(z2n) >>> ', fg='blue', bold=True), intro=globals.__intro__)
def z2n():
    """
    This program allows the user to calculate periodograms using the Z2n
    statistics a la Buccheri et al. 1983 from fits datasets.

    The standard Z2n statistics calculates the phase of each photon and
    the sinusoidal functions above for each photon. Be advised that this
    is very computationally expensive if the number of photons is high.
    """


@z2n.command()
def docs() -> None:
    """
    Open the documentation on the software (type docs).
    """

    try:

        click.launch(globals.__docs__)

    except Exception as error:
        click.secho(f'{error}', fg='red')

    click.echo(f"To read the documentation go to {globals.__docs__}")


@z2n.command()
def plot() -> None:
    """
    Open the interactive plotting window (type plot).
    """

    if globals.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        globals.plot()

        cli.plot()


@z2n.command()
def run() -> None:
    """
    Calculate the Z2n periodogram (type run).
    """

    if(globals.fits != 0):

        if(click.confirm("Do you want to use another file")):

            path = click.prompt("Path to fits file")

            globals.time = file.load_fits(path)

            try:

                if(globals.time.size != 0):
                    click.secho("Fits file loaded correctly.", fg='green')
                    globals.fits = 1

            except Exception as error:
                click.secho(f'{error}', fg='red')

            else:

                try:

                    if(click.confirm("Do you want to run with the default values")):

                        oversample = click.prompt(
                            "Frequency steps", type=float)
                        globals.frequency = stats.frequency(globals.time)
                        globals.fmin = globals.frequency * 2
                        globals.fmax = globals.frequency * 100
                        globals.delta = oversample

                    else:

                        globals.fmin = click.prompt(
                            "Minimum frequency", type=float)
                        globals.fmax = click.prompt(
                            "Maximum frequency", type=float)
                        globals.delta = click.prompt(
                            "Frequency steps", type=float)

                    globals.z2n()

                except Exception as error:
                    click.secho(
                        f'Failed to calculate the parameters.', fg='red')

        else:
            click.secho("If you want to recalculate (type axis).", fg='yellow')

    else:

        path = click.prompt("Path to fits file")

        globals.time = file.load_fits(path)

        try:

            if(globals.time.size != 0):
                click.secho("Fits file loaded correctly.", fg='green')
                globals.fits = 1

        except Exception as error:
            click.secho(f'{error}', fg='red')

        else:

            try:

                if(click.confirm("Do you want to run with the default values")):

                    oversample = click.prompt("Frequency steps", type=float)
                    globals.frequency = stats.frequency(globals.time)
                    globals.fmin = globals.frequency * 2
                    globals.fmax = globals.frequency * 100
                    globals.delta = oversample

                else:

                    globals.fmin = click.prompt(
                        "Minimum frequency", type=float)
                    globals.fmax = click.prompt(
                        "Maximum frequency", type=float)
                    globals.delta = click.prompt("Frequency steps", type=float)

                globals.z2n()

            except Exception as error:
                click.secho(f'Failed to calculate the parameters.', fg='red')
                globals.fits = 0


@z2n.command()
def axis() -> None:
    """
    Change the axis used on the periodogram (type axis).
    """

    if globals.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        click.secho("This will recalculate the periodogram.", fg='yellow')

        opt = click.prompt(
            "Recalculate the whole region [1] or just the region selected [2]")

        if(opt == '1'):

            if(click.confirm("Did you already select the new limits")):

                ax = plt.gca().get_xlim()

                globals.fmin = ax[0]
                globals.fmax = ax[1]
                globals.delta = click.prompt("Frequency steps", type=float)

                globals.frequencies = np.arange(
                    globals.fmin, globals.fmax, globals.delta)

                globals.z2n()

        elif(opt == '2'):

            if(click.confirm("Did you already select the region")):

                ax = plt.gca().get_xlim()

                i = np.where(np.isclose(globals.frequencies, ax[0], 0.1))
                j = np.where(np.isclose(globals.frequencies, ax[1], 0.1))
                l = np.rint(np.median(i)).astype(int)
                u = np.rint(np.median(j)).astype(int)
                size = u - l

                fmin = ax[0]
                fmax = ax[1]
                delta = click.prompt("Frequency steps", type=float)
                freq = np.arange(fmin, fmax, delta)

                try:

                    period = stats.periodogram(globals.time, freq)
                    click.secho(
                        f'Finished to calculate the periodogram.', fg='green')

                except:
                    click.secho(
                        f'Failed to calculate the periodogram.', fg='red')

                else:
                    t = (globals.frequencies.size - size) + freq.size
                    p = l + freq.size

                    tempx = np.zeros(t)
                    tempy = np.zeros(t)

                    tempx[:l] = globals.frequencies[:l]
                    tempy[:l] = globals.periodogram[:l]
                    tempx[l:p] = freq
                    tempy[l:p] = period
                    tempx[p:] = globals.frequencies[u:]
                    tempy[p:] = globals.periodogram[u:]

                    globals.frequencies = tempx
                    globals.periodogram = tempy

                    globals.plot()

        else:
            click.secho(f"Select '1' or '2'.", fg='red')


@z2n.command()
def back() -> None:
    """
    Create subplot of a background file (type back).
    """

    if globals.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        if(globals.axis != 0):

            opt = click.prompt(
                "Do you want to change the background [1] or remove it [2]")

            if(opt == '1'):

                path = click.prompt("Path to background file")

                globals.background = file.load_fits(path)

                try:

                    if(globals.background.size != 0):
                        click.secho(
                            "Background file loaded correctly.", fg='green')
                        globals.axis = 1
                        globals.plot()

                except Exception as error:
                    click.secho(f'{error}', fg='red')

            elif(opt == '2'):
                click.secho(
                    "Background file removed.", fg='green')
                globals.axis = 0
                globals.plot()

            else:
                click.secho(f"Select '1' or '2'.", fg='red')

        else:

            path = click.prompt("Path to background file")

            globals.background = file.load_fits(path)

            try:

                if(globals.background.size != 0):
                    click.secho(
                        "Background file loaded correctly.", fg='green')
                    globals.axis = 1
                    globals.plot()

            except Exception as error:
                click.secho(f'{error}', fg='red')


@z2n.command()
def save() -> None:
    """
    Save the periodogram into a file (type save).
    """

    if globals.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        txt = click.prompt("Name of the output file")

        out = click.prompt("Which format [ascii, csv, fits]")

        if out == 'ascii':
            file.save_ascii(globals.frequencies, globals.periodogram, txt)

        elif out == 'csv':
            file.save_csv(globals.frequencies, globals.periodogram, txt)

        elif out == 'fits':
            file.save_fits(globals.frequencies, globals.periodogram, txt)

        else:
            click.secho(f"{out} format not supported.", fg='red')
