#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
from click_shell import shell

# Other Libraries
import globals
import subprocess
from file import fits
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

    for line in globals.__credits__:
        click.echo("\n%s\n" %line)

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
@click.option('--path', '-p', type=click.Path(), help='Path to fits file.')
def file(path):
    """
    Open fits and stores photon arrival times (type file -p <path>).
    """

    globals.time = fits.load_fits(path)

    try:
        if globals.time.size != 0:
            click.echo("\nPhoton arrival times.\n")
            click.echo(globals.time)
            click.echo("\nFits file loaded correctly. Try run stats command for statistics.\n")
    except:
        pass

@cli.command()
def stats():
    """
    Applies the Z2n stats to photon arrival times (type stats).
    """

    if globals.time.size == 0:
        click.echo("\nNo fits files were loaded yet. Try run file command.\n")

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
@click.option('--title', '-t', type=str, help='Title of the output file.')
@click.option('--xlabel', '-x', type=str, help='X label of the output file.')
@click.option('--ylabel', '-y', type=str, help='Y label of the output file.')
@click.option('--name', '-n', type=str, help='Name of the output file.')
def figure(title, xlabel, ylabel, name):
    """
    Plots the periodogram into an output file (type figure -n <file>).
    """

    globals.figure.set_title(title)
    globals.figure.set_xlabel(xlabel)
    globals.figure.set_yabel(ylabel)
    globals.figure.set_file(name)

    if globals.periodogram.size == 0:
        click.echo("\nThe Z2n statistics were not calculated yet. Try run stats command.\n")
    
    else:
        plot.savefig(globals.frequencies, globals.periodogram, globals.figure)
        click.echo("\nFile saved at %s.png.\n" %globals.figure.file)

@cli.command()
@click.option('--command', '-c', type=str, help='Shell command to be prompted.')
def shell(command):
    """
    Provides a quick acess to bash commands (type shell -c <command>).
    """
    
    pipe = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)

    pipe.stdin.write(command)
    pipe.stdin.close()

    for line in pipe.stdout:
        click.echo(line)