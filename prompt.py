#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
import globals
import subprocess
from click_shell import shell
from file.fits import load_fits
from stats import z2n
from figure import plot

@shell(prompt = '(z2n) >>> ', intro = globals.intro)
#@click.option('--fits', '-f', type=(click.Path()), help='Path to fits file.')
#@click.option('--read', '-r', type=(click.Path()), help='Path to script file.')
def cli():
    """
    A python package for optimized Z2n periodograms from fits datasets

    For more information go to https://z2n-periodogram.github.io
    """

@cli.command()
def copyright():
    """
    Shows copyright of the software (type copyright).
    """
    click.echo("\n%s\nAll Rights Reserved.\n" %globals.__copyright__)

@cli.command()
def version():
    """
    Shows the current version of the Z2n software (type version).
    """

    click.echo("\nZ2n %s\n" %globals.__version__)

@cli.command()
def credits():
    """
    Shows the credits of the software (type credits).
    """

    click.echo("\n%s\n" %globals.__credits__)

@cli.command()
def license():
    """
    Shows the current software license (type license).
    """

    with open("LICENSE", "r") as file:
        license = file.readlines()
    
    for line in license:
        click.echo(line)

@cli.command()
def fits():
    """
    Open file and stores photon arrival times (type fits <path>).
    """

    globals.time = load_fits()

    try:
        if globals.time.size != 0:
            click.echo("\nPhoton arrival times.\n")
            click.echo(globals.time)
            click.echo("\nFits file loaded correctly. Try run z2n command for statistics.\n")
    except:
        pass

@cli.command()
def z2n():
    """
    Applies the Z2n statistics to photon arrival times (type z2n).
    """

    if globals.time.size == 0:
        click.echo("\nNo fits files were loaded yet. Try run fits command.\n")

    else:
        click.echo("\nCalculating phase values.\n")
        globals.phase = z2n.phases(globals.time, globals.frequencies)
        click.echo("\n")            
        click.echo(globals.phase)
        click.echo("\nApplying the Z2n statistics.\n")
        globals.periodogram = z2n.periodogram(globals.phase, globals.frequencies)
        click.echo("\n")
        click.echo(globals.periodogram)
        click.echo("\n")

@cli.command()
def plot():
    """
    Plots the periodogram into an output file (type plot <file>).
    """

    if globals.periodogram.size == 0:
        click.echo("\nThe Z2n statistics were not calculated yet. Try run z2n command.\n")
    
    else:
        plot.plot(globals.frequencies, globals.periodogram)

@cli.command()
def shell():
    """
    Provides a quick acess to bash commands (type shell <command>).
    """
    
    pipe = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)

    pipe.stdin.write(args)
    pipe.stdin.close()

    for line in pipe.stdout:
        click.echo(line)