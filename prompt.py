#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import subprocess
from fits.fits import load_fits
from stats import z2n
from figure import plot
from cmd import Cmd
class z2n_prompt(Cmd):

    def do_copyright(self, args):
        """
        Shows copyright of the software (type copyright).
        """

        click.echo("\nCopyright (c) 2019 Yohan Alexander.\nAll Rights Reserved.\n")

    def do_credits(self, args):
        """
        Shows the credits of the software (type credits).
        """

        click.echo("""\nA python package for optimized Z2n periodograms from fits datasets.
        \nFor more information go to https://z2n-periodogram.github.io\n""")

    def do_license(self, args):
        """
        Shows license under which the software is under (type license).
        """
        with open("LICENSE", "r") as file:
            license = file.readlines()
        
        for line in license:
            click.echo(line)
                
    def do_fits(self, args):
        """
        Open fits files and loads photon arrival times into variable (type fits <path>).
        """

        time = load_fits(args)
        click.echo("\nPhoton arrival times\n")
        click.echo(time)
    
    def do_phases(self, args):
        """
        Calculates phase values from photon arrival times (type phases <times> <freq>).
        """

        phase = z2n.phases(args)

    def do_z2n(self, args):
        """
        Applies the Z2n statistics to phase values and normalize (type z2n <times> <freq>).
        """

        stats = z2n.periodogram(args)

    def do_plot(self, args):
        """
        Plots the periodogram into an output file (type plot <file>).
        """

        plot.plot(args)

    def do_quit(self, args):
        """
        Quits the software interactive command prompt (type quit).
        """

        click.echo("\nQuitting the Z2n Peridogram Software.\n")

        raise SystemExit

    def do_bash(self, args):
        """
        Provides a quick acess to bash commands using pipe (type bash <command>).
        """

        pipe = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)

        pipe.stdin.write(args)
        pipe.stdin.close()

        for line in pipe.stdout:
            print(line)