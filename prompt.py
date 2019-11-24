#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import globals
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from file import fits
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

@shell(prompt = '(z2n) >>> ', intro = globals.intro)
def cli():
    """
    A python package for optimized Z2n periodograms from fits datasets.
    """

@cli.command()
def plot():
    """
    Opens the interactive plotting window (type plot).
    """

    if globals.periodogram.size == 0:
        click.echo("The frequency spectrum was not calculated yet. Try run stats command.")

    else:

        plt.ion()
        plt.tight_layout()
        plt.plot(globals.frequencies, globals.periodogram, label="Z2n Statistics")
        plt.legend()
        plt.show()
    
        globals.Plot().cmdloop()


@cli.command()
@click.option('--run', '-r', type=(click.Path()), help='Path to fits file.')
def auto(run):
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
            click.echo("Photon arrival times.")
            click.echo(globals.time)
            
            globals.period = z2n.period(globals.time)
            click.echo("Period of the signal: %f s" %globals.period)

            globals.frequency = z2n.frequency(globals.time)
            click.echo("Sampling Frequency of the signal: %f Hz" %globals.frequency)

            globals.fmin = globals.frequency
            globals.fmax = globals.frequency * 100
            globals.delta =  ((1 / oversample) / globals.period)
            click.echo("Minimum frequency used on the spectrum: %s Hz" %globals.fmin)
            click.echo("Maximum frequency used on the spectrum: %s Hz" %globals.fmax)
            click.echo("Frequency step used on the spectrum: %s Hz" %globals.delta)
            globals.frequencies = np.arange(globals.fmin, globals.fmax, globals.delta)

            click.echo("Calculating phase values.")
            globals.phase = z2n.phases(globals.time, globals.frequencies)
            
            click.echo("Applying the Z2n statistics.")
            globals.periodogram = z2n.periodogram(globals.phase, globals.frequencies)

            fig.savefig(globals.frequencies, globals.periodogram, "z2n")

            click.echo("Image file saved at z2n.png")

            with open('z2n.txt', 'w') as file:
                for spec, freq in zip(globals.periodogram, globals.frequencies):
                    file.write(str(freq) + " " + str(spec) + "\n")
            
            click.echo("Text file saved at z2n.txt")

        except Exception as error:
            click.echo(error)

@cli.command()
def docs():
    """
    Opens the documentation on the software (type docs).
    """

    globals.webbrowser.open(globals.__url__)

    click.echo("To read the documentation on the software go to %s" %globals.__url__)

@cli.command()
def copyright():
    """
    Shows copyright of the software (type copyright).
    """
    
    click.echo("%sAll Rights Reserved." %globals.__copyright__)

@cli.command()
def version():
    """
    Shows the current version of the Z2n software (type version).
    """

    click.echo("Z2n %s" %globals.__version__)

@cli.command()
def credits():
    """
    Shows the credits of the software (type credits).
    """

    for line in globals.__credits__:
        click.echo("%s" %line)

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
def data(path):
    """
    Open fits and stores photon arrival times (type file).
    """

    if(path is None):
        path = input("Path to fits file: ")

    globals.time = fits.load_fits(path)

    try:
        
        if globals.time.size != 0:
            click.echo("Photon arrival times.")
            click.echo(globals.time)
            click.echo("Fits file loaded correctly. Try run rate command.")

    except Exception as error:
        click.echo(error)

@cli.command()
@click.option('--fmin', '-fm', type=int, help="Minimum frequency of the spectrum.")
@click.option('--fmax', '-fx', type=int, help="Maximum frequency of the spectrum.")
@click.option('--delta', '-d', type=int, help="Frequency steps of the spectrum.")
def rate(fmin, fmax, delta):
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
def stats():
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
def ascii(text):
    """
    Saves the frequency spectrum into an text file (type ascii).
    """

    if globals.periodogram.size == 0:
        click.echo("The frequency spectrum was not calculated yet. Try run stats command.")

    else:
        
        if(text is None):
            text = input("Name of the output file: ")
        
        with open('%s.txt' %text, 'w') as file:

            for spec, freq in zip(globals.periodogram, globals.frequencies):
                file.write(str(freq) + " " + str(spec) + "\n")
        
        click.echo("Text file saved at %s.txt" %text)

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
        click.echo("File saved at %s.png" %name)

@cli.command()
@click.option('--command', '-c', type=str, help='Shell command to be prompted.')
def shell(command):
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