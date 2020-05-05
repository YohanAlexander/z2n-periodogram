#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt
from click_shell import shell

# Other Libraries
import z2n.globals as glob
import z2n.stats as stats
import z2n.main as main
import z2n.file as file
import z2n.plot as cli


@click.version_option(prog_name="Z2n Software", version=glob.__version__)
@shell(prompt=click.style('(z2n) >>> ', fg='blue', bold=True), intro=glob.__intro__)
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
    """Open the documentation on the software (type docs)."""

    try:

        click.launch(glob.__docs__)

    except Exception as error:
        click.secho(f'{error}', fg='red')

    click.echo(f"To read the documentation go to {glob.__docs__}")


@z2n.command()
def plot() -> None:
    """Open the interactive plotting window (type plot)."""

    if glob.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        main.plot()

        cli.plot()


@z2n.command()
def run() -> None:
    """Calculate the Z2n periodogram (type run)."""

    if glob.fits != 0:

        if click.confirm("Do you want to use another file"):

            path = click.prompt("Path to fits file")

            glob.time = file.load_fits(path)

            try:

                if glob.time.size != 0:
                    click.secho("Fits file loaded correctly.", fg='green')
                    glob.fits = 1

            except Exception as error:
                click.secho(f'{error}', fg='red')

            else:

                try:

                    if click.confirm("Do you want to run with the default values"):

                        oversample = click.prompt(
                            "Frequency steps", type=float)
                        glob.frequency = stats.frequency(glob.time)
                        glob.fmin = glob.frequency * 2
                        glob.fmax = glob.frequency * 100
                        glob.delta = oversample

                    else:

                        glob.fmin = click.prompt(
                            "Minimum frequency", type=float)
                        glob.fmax = click.prompt(
                            "Maximum frequency", type=float)
                        glob.delta = click.prompt(
                            "Frequency steps", type=float)

                    main.z2n()

                except Exception as error:
                    click.secho(
                        "Failed to calculate the parameters.", fg='red')

        else:
            click.secho("If you want to recalculate (type axis).", fg='yellow')

    else:

        path = click.prompt("Path to fits file")

        glob.time = file.load_fits(path)

        try:

            if glob.time.size != 0:
                click.secho("Fits file loaded correctly.", fg='green')
                glob.fits = 1

        except Exception as error:
            click.secho(f'{error}', fg='red')

        else:

            try:

                if click.confirm("Do you want to run with the default values"):

                    oversample = click.prompt("Frequency steps", type=float)
                    glob.frequency = stats.frequency(glob.time)
                    glob.fmin = glob.frequency * 2
                    glob.fmax = glob.frequency * 100
                    glob.delta = oversample

                else:

                    glob.fmin = click.prompt(
                        "Minimum frequency", type=float)
                    glob.fmax = click.prompt(
                        "Maximum frequency", type=float)
                    glob.delta = click.prompt("Frequency steps", type=float)

                main.z2n()

            except Exception as error:
                click.secho("Failed to calculate the parameters.", fg='red')
                glob.fits = 0


@z2n.command()
def axis() -> None:
    """Change the axis used on the periodogram (type axis)."""

    if glob.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        click.secho("This will recalculate the periodogram.", fg='yellow')

        opt = click.prompt(
            "Recalculate the whole region [1] or just the region selected [2]")

        if opt == '1':

            if click.confirm("Did you already select the new limits"):

                ax = plt.gca().get_xlim()

                glob.fmin = ax[0]
                glob.fmax = ax[1]
                glob.delta = click.prompt("Frequency steps", type=float)

                glob.frequencies = np.arange(
                    glob.fmin, glob.fmax, glob.delta)

                main.z2n()

        elif opt == '2':

            if click.confirm("Did you already select the region"):

                ax = plt.gca().get_xlim()

                ax_x = np.where(np.isclose(glob.frequencies, ax[0], 0.1))
                ax_y = np.where(np.isclose(glob.frequencies, ax[1], 0.1))
                lower = np.rint(np.median(ax_x)).astype(int)
                uppper = np.rint(np.median(ax_y)).astype(int)
                size = uppper - lower

                fmin = ax[0]
                fmax = ax[1]
                delta = click.prompt("Frequency steps", type=float)
                freq = np.arange(fmin, fmax, delta)

                try:

                    period = stats.periodogram(glob.time, freq)
                    click.secho(
                        "Finished to calculate the periodogram.", fg='green')

                except Exception as error:
                    click.secho(
                        "Failed to calculate the periodogram.", fg='red')

                else:
                    total = (glob.frequencies.size - size) + freq.size
                    final = lower + freq.size

                    tempx = np.zeros(total)
                    tempy = np.zeros(total)

                    tempx[:lower] = glob.frequencies[:lower]
                    tempy[:lower] = glob.periodogram[:lower]
                    tempx[lower:final] = freq
                    tempy[lower:final] = period
                    tempx[final:] = glob.frequencies[uppper:]
                    tempy[final:] = glob.periodogram[uppper:]

                    glob.frequencies = tempx
                    glob.periodogram = tempy

                    main.plot()

        else:
            click.secho("Select '1' or '2'.", fg='red')


@z2n.command()
def back() -> None:
    """Create subplot of a background file (type back)."""

    if glob.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        if glob.axis != 0:

            opt = click.prompt(
                "Do you want to change the background [1] or remove it [2]")

            if opt == '1':

                path = click.prompt("Path to background file")

                glob.background = file.load_fits(path)

                try:

                    if glob.background.size != 0:
                        click.secho(
                            "Background file loaded correctly.", fg='green')
                        glob.axis = 1
                        main.plot()

                except Exception as error:
                    click.secho(f'{error}', fg='red')

            elif opt == '2':
                click.secho(
                    "Background file removed.", fg='green')
                glob.axis = 0
                main.plot()

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:

            path = click.prompt("Path to background file")

            glob.background = file.load_fits(path)

            try:

                if glob.background.size != 0:
                    click.secho(
                        "Background file loaded correctly.", fg='green')
                    glob.axis = 1
                    main.plot()

            except Exception as error:
                click.secho(f'{error}', fg='red')


@z2n.command()
def save() -> None:
    """Save the periodogram into a file (type save)."""

    if glob.periodogram.size == 0:
        click.secho("The periodogram was not calculated yet.", fg='yellow')

    else:

        txt = click.prompt("Name of the output file")

        out = click.prompt("Which format [ascii, csv, fits]")

        if out == 'ascii':
            file.save_ascii(glob.frequencies, glob.periodogram, txt)

        elif out == 'csv':
            file.save_csv(glob.frequencies, glob.periodogram, txt)

        elif out == 'fits':
            file.save_fits(glob.frequencies, glob.periodogram, txt)

        else:
            click.secho(f"{out} format not supported.", fg='red')
