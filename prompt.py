#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import globals
import subprocess
from file import fits
from stats import z2n
from figure import plot

# Other Libraries
import click
from click_shell import shell

@shell(prompt = '(z2n) >>> ', intro = globals.intro)
def cli():
    """
    A python package for optimized Z2n periodograms from fits datasets

    For more information go to https://z2n-periodogram.readthedocs.io
    """

@cli.command()
@click.option('--run', '-r', type=(click.Path()), help='Path to fits file.')
def auto(run):
    """
    Run Z2n statistics with the default values (type auto).
    """

    if(click.confirm("Do you wish to auto run with the default values?")):
       
        if(run is None):
           run = input("\nPath to fits file: ")
        
        try:
            oversample = int(input("\nOver sampling of the frequency steps: "))
            if type(oversample) != int:
                raise Exception
        except:
            print("\nInvalid value of steps.\n")
       
        try:
            globals.time = fits.load_fits(run)
            size = z2n.period(globals.time) * (1 / oversample)
            click.echo("\nPhoton arrival times.\n")
            click.echo(globals.time)
            click.echo("\nCalculating the Nyquist frequency.\n")
            globals.sample_rate = z2n.nyquist(globals.time)
            click.echo(globals.sample_rate)
            globals.frequencies = globals.np.arange(1e-4, 1.5e-3, 1e-5)
            click.echo("\nMaximum frequency used on the spectrum: %s" %globals.fmax)
            click.echo("\nMinimum frequency used on the spectrum: %s" %globals.fmin)
            click.echo("\nFrequency step used on the spectrum: %s" %globals.delta)
            click.echo("\nCalculating phase values.\n")
            globals.phase = z2n.phases(globals.time, globals.frequencies)
            click.echo("\n")
            click.echo(globals.phase)
            click.echo("\nApplying the Z2n statistics.\n")
            globals.periodogram = z2n.periodogram(globals.phase, globals.frequencies)
            click.echo("\n")
            click.echo(globals.periodogram)
            globals.figure.set_title("Z2n Periodogram")
            globals.figure.set_xlabel("Frequencies (Hz)")
            globals.figure.set_yabel("Amplitude")
            globals.figure.set_file("z2n")
            plot.savefig(globals.frequencies, globals.periodogram, globals.figure)
            click.echo("\nImage file saved at %s.png.\n" %globals.figure.file)
            with open('%s.txt' %globals.figure.file, 'w') as file:
                for spec, freq in zip(globals.periodogram, globals.frequencies):
                    file.write(str(freq) + " " + str(spec) + "\n")
            click.echo("\nText file saved at %s.txt.\n" %globals.figure.file)

        except:
            pass

@cli.command()
def docs():
    """
    Opens the documentation on the software (type docs).
    """

    globals.webbrowser.open('https://z2n-periodogram.readthedocs.io')

    click.echo("\nTo read the documentation on the software go to https://z2n-periodogram.readthedocs.io\n")

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
    Open fits and stores photon arrival times (type file).
    """

    if(path is None):
        path = input("\nPath to fits file: ")

    globals.time = fits.load_fits(path)

    try:
        if globals.time.size != 0:
            click.echo("\nPhoton arrival times.\n")
            click.echo(globals.time)
            click.echo("\nFits file loaded correctly. Try run rate command.\n")
    except:
        pass

@cli.command()
@click.option('--fmin', '-fm', type=int, help="Minimum frequency of the spectrum.")
@click.option('--fmax', '-fx', type=int, help="Maximum frequency of the spectrum.")
@click.option('--delta', '-d', type=int, help="Frequency steps of the spectrum.")
def rate(fmin, fmax, delta):
    """
    Defines the bandwidth of the spectrum frequency (type rate).
    """

    if(globals.time.size == 0):
        click.echo("\nNo fits files were loaded yet. Try run file command.\n")

    else:

        if(fmin is None):
            fmin = float(input("\nMinimum frequency of the spectrum: "))
    
        if(fmax is None):
            fmax = float(input("\nMaximum frequency of the spectrum: "))

        if(delta is None):
            delta = float(input("\nFrequency steps of the spectrum: "))
        
        globals.frequencies = globals.np.arange(fmin, fmax, delta)

@cli.command()
def stats():
    """
    Applies the Z2n stats to photon arrival times (type stats).
    """

    if globals.time.size == 0:
        click.echo("\nNo fits files were loaded yet. Try run file command.\n")

    elif globals.frequencies.size == 0:
        click.echo("\nThe frequency spectrum was not defined yet. Try run rate command.\n")

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
@click.option('--text', '-t', type=str, help='Name of the output file.')
def ascii(text):
    """
    Saves the frequency spectrum into an text file (type ascii).
    """

    if globals.periodogram.size == 0:
        click.echo("\nThe frequency spectrum was not calculated yet. Try run stats command.\n")

    else:
        
        if(text is None):
            text = input("\nName of the output file: ")
        
        with open('%s.txt' %text, 'w') as file:

            for spec, freq in zip(globals.periodogram, globals.frequencies):
                file.write(str(freq) + " " + str(spec) + "\n")


@cli.command()
@click.option('--title', '-t', type=str, help='Title to plot on the image.')
@click.option('--xlabel', '-x', type=str, help='X label to plot on the image.')
@click.option('--ylabel', '-y', type=str, help='Y label to plot on the image.')
@click.option('--name', '-n', type=str, help='Name of the output file.')
def figure(title, xlabel, ylabel, name):
    """
    Plots the periodogram into a image file (type figure).
    """

    if globals.periodogram.size == 0:
        click.echo("\nThe frequency spectrum was not calculated yet. Try run stats command.\n")

    else:

        if(title is None):
            title = input("\nTitle to plot on the image: ")

        if(xlabel is None):
            xlabel = input("\nX label to plot on the image: ")

        if(ylabel is None):
            ylabel = input("\nY label to plot on the image: ")

        if(name is None):
            name = input("\nName of the output file: ")

        globals.figure.set_title(title)
        globals.figure.set_xlabel(xlabel)
        globals.figure.set_yabel(ylabel)
        globals.figure.set_file(name)
        
        plot.savefig(globals.frequencies, globals.periodogram, globals.figure)
        click.echo("\nFile saved at %s.png.\n" %globals.figure.file)

@cli.command()
@click.option('--command', '-c', type=str, help='Shell command to be prompted.')
def shell(command):
    """
    Provides a quick acess to bash commands (type shell).
    """

    if(command is None):
        command = input("\nType the shell command: ")
    
    pipe = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)

    pipe.stdin.write(command)
    pipe.stdin.close()

    for line in pipe.stdout:
        click.echo(line)