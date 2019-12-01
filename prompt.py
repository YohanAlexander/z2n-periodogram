#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in

import globals
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from file import fits, txt
from stats import z2n
from figure import fig

# Plotting Style

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

# Other Libraries

import click
from click_shell import shell

@shell(prompt = '(z2n) >>> ', intro = globals.__intro__)
def cli():
    """
    A python package for optimized Z2n periodograms from fits datasets.

    This program allows the user to calculate periodograms using the Z2n statistics
    a la Buccheri et al. 1983.

    The standard Z2n statistics calculates the phase of each photon and the 
    sinusoidal functions above for each photon. Be advised that this is very 
    computationally expensive if the number of photons is high.

    This program accepts fits files (.fits) and it is assumed that contains
    a header with the event or time series data.

    This program requires that `requirements.txt` be installed within the Python
    environment you are running this program in.

    This program can also be imported as a module and contains the functions
    described in the documentation available at:

    https://z2n-periodogram.readthedocs.io
    """

@cli.command()
def plot() -> None:
    """
    Opens the interactive plotting window (type plot).
    """

    if globals.periodogram.size == 0:
        click.echo("The frequency spectrum was not calculated yet. Try run stats command.")

    else:

        plt.close()
        plt.ion()
        plt.tight_layout()
        plt.plot(globals.frequencies, globals.periodogram, label="Z2n Statistics")
        plt.legend()
        plt.show()
    
        globals.Plot().cmdloop()

@cli.command()
@click.option('--run', '-r', type=(click.Path()), help='Path to a fits file.')
def auto(run: str) -> None:
    """
    Run Z2n statistics with the default values (type auto).
    """

    if(click.confirm("Do you wish to auto run with the default values?")):
       
        if(run is None):
           run = input("Path to fits file: ")
        
        try:
            oversample = int(input("Frequency steps (delta): "))
            if type(oversample) != int:
                raise Exception

        except Exception as error:
            print(error)
       
        try:
            
            globals.time = fits.load_fits(run)
            click.echo(f"Photon arrival times: {globals.time}")
            
            globals.period = z2n.period(globals.time)
            click.echo(f"Period of observation on the signal: {globals.period} s")

            globals.frequency = z2n.frequency(globals.time)
            click.echo(f"Sampling Frequency of the signal: {globals.frequency} Hz")

            globals.fmin = globals.frequency
            globals.fmax = globals.frequency * 100
            globals.delta =  ((1 / oversample) / globals.period)
            click.echo(f"Minimum frequency used on the spectrum: {globals.fmin} Hz")
            click.echo(f"Maximum frequency used on the spectrum: {globals.fmax} Hz")
            click.echo(f"Frequency steps used on the spectrum: {globals.delta} Hz")
            
            globals.frequencies = np.arange(globals.fmin, globals.fmax, globals.delta)

            globals.phase = z2n.phases(globals.time, globals.frequencies)

            globals.periodogram = z2n.periodogram(globals.phase, globals.frequencies)

            globals.peak = z2n.peak(globals.periodogram, globals.frequencies)
            click.echo(f"Peak value of the spectrum: {globals.peak} Hz")

            fig.save_fig(globals.frequencies, globals.periodogram, "z2n")

            txt.save_ascii(globals.periodogram, globals.frequencies, "z2n")

            globals.Plot().cmdloop()

        except Exception as error:
            click.echo(error)

@cli.command()
def docs() -> None:
    """
    Opens the documentation on the software (type docs).
    """

    globals.webbrowser.open(globals.__url__)

    click.echo(f"To read the documentation on the software go to {globals.__url__}")

@cli.command()
def copyright() -> None:
    """
    Shows copyright of the software (type copyright).
    """
    
    click.echo(f"{globals.__copyright__}\nAll Rights Reserved.")

@cli.command()
def version() -> None:
    """
    Shows the current version of the Z2n software (type version).
    """

    click.echo(f"Z2n Software {(globals.__version__)}")

@cli.command()
def credits() -> None:
    """
    Shows the credits of the software (type credits).
    """

    for line in globals.__credits__:
        click.echo(f"{line}")

@cli.command()
def license() -> None:
    """
    Shows the current software license (type license).
    """

    with open("LICENSE", "r") as file:
        license = file.readlines()
    
    for line in license:
        click.echo(line)

@cli.command()
@click.option('--path', '-p', type=click.Path(), help='Path to a fits file.')
def data(path: str) -> None:
    """
    Open fits and stores photon arrival times (type data).
    """

    if(path is None):
        path = input("Path to fits file: ")

    globals.time = fits.load_fits(path)

    try:
        
        if globals.time.size != 0:
            click.echo(f"Photon arrival times: {globals.time}")
            click.echo("Fits file loaded correctly. Try run rate command.")

    except Exception as error:
        click.echo(error)

@cli.command()
@click.option('--fmin', '-fm', type=float, help="Minimum frequency of the spectrum.")
@click.option('--fmax', '-fx', type=float, help="Maximum frequency of the spectrum.")
@click.option('--delta', '-d', type=float, help="Frequency steps of the spectrum.")
def rate(fmin: float, fmax: float, delta: float) -> None:
    """
    Defines the bandwidth of the spectrum frequency (type rate).
    """

    if(globals.time.size == 0):
        click.echo("No fits files were loaded yet. Try run data command.")

    else:

        if(fmin is None):
            fmin = float(input("Minimum frequency of the spectrum: "))
    
        if(fmax is None):
            fmax = float(input("Maximum frequency of the spectrum: "))

        if(delta is None):
            delta = float(input("Frequency steps of the spectrum: "))
        
        globals.frequencies = np.arange(fmin, fmax, delta)

@cli.command()
def stats() -> None:
    """
    Applies the Z2n stats to photon arrival times (type stats).
    """

    if globals.time.size == 0:
        click.echo("No fits files were loaded yet. Try run data command.")

    elif globals.frequencies.size == 0:
        click.echo("The frequency spectrum was not defined yet. Try run rate command.")

    else:
        click.echo("Calculating phase values.")
        globals.phase = z2n.phases(globals.time, globals.frequencies)

        click.echo("Applying the Z2n statistics.")
        globals.periodogram = z2n.periodogram(globals.phase, globals.frequencies)

@cli.command()
@click.option('--text', '-t', type=str, help='Name of the output file.')
def text(text: str) -> None:
    """
    Saves the frequency spectrum into an ascii file (type text).
    """

    if globals.periodogram.size == 0:
        click.echo("The frequency spectrum was not calculated yet. Try run stats command.")

    else:
        
        if(text is None):
            text = input("Name of the output file: ")
        
        ascii.save_ascii(text)

@cli.command()
@click.option('--title', '-t', type=str, help='Title to plot on the image.')
@click.option('--xlabel', '-x', type=str, help='X label to plot on the image.')
@click.option('--ylabel', '-y', type=str, help='Y label to plot on the image.')
@click.option('--name', '-n', type=str, help='Name of the output file.')
def figure(title: str, xlabel: str, ylabel: str, name: str) -> None:
    """
    Plots the periodogram into a image file (type figure).
    """

    if globals.periodogram.size == 0:
        click.echo("The frequency spectrum was not calculated yet. Try run stats command.")

    else:

        if(title is None):
            title = input("Title to plot on the image: ")

        if(xlabel is None):
            xlabel = input("X label to plot on the image: ")

        if(ylabel is None):
            ylabel = input("Y label to plot on the image: ")

        if(name is None):
            name = input("Name of the output file: ")

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        fig.savefig(globals.frequencies, globals.periodogram, name)

@cli.command()
@click.option('--command', '-c', type=str, help='Shell command to be prompted.')
def shell(command: str) -> None:
    """
    Provides a quick acess to bash commands (type shell).
    """

    if(command is None):
        command = input("Type the shell command: ")
    
    pipe = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)

    pipe.stdin.write(command)
    pipe.stdin.close()

    for line in pipe.stdout:
        click.echo(line.strip())
