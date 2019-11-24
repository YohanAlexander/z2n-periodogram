#! /usr/bin/python
# -*- coding: utf-8 -*-

# Wrapping Header
__author__ = 'Yohan Alexander'
__version__ = '0.3.0'
__copyright__ = 'Copyright (C) 2019, Z2n Software, by Yohan Alexander.'
__credits__ = ['''The Z2n Software was developed by Yohan Alexander and it is supported by the Open Source community.''']
__license__ = 'MIT LICENSE'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'
__url__ = "https://z2n-periodogram.readthedocs.io"

intro = """
        Z2n Software (%s), a python package for optimized periodograms.
        Copyright (C) 2019, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.

        If you wish to run the software with the default values type auto.
        """ %__version__

# Generic/Built-in
import time, sys, os, functools, webbrowser

# Other Libraries
import cmd
import click
import prompt
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Global Objects
class Plot(cmd.Cmd):
    
    prompt = '(plt) >>>'
    intro = """
            Interactive plotting window of the Z2n Software.
            Type "help" for more information.
            """

    def do_grid(self, args):
        """
        Plots grid on the figure (type grid <True>).
        """

        plt.grid(args)

    def do_title(self, args):
        """
        Changes the title (type title <title>).
        """

        plt.title(args)

    def do_xlabel(self, args):
        """
        Changes the xlabel (type xlabel <xlabel>).
        """

        plt.xlabel(args)

    def do_xlim(self, args):
        """
        Changes the xlim (type xlim <xlim>).
        """

        plt.xlim(args)
    
    def do_xscale(self, args):
        """
        Changes the xscale (type xscale <xscale>).
        """

        plt.xscale(args)

    def do_ylabel(self, args):
        """
        Changes the ylabel (type ylabel <ylabel>).
        """

        plt.ylabel(args)

    def do_ylim(self, args):
        """
        Changes the ylim (type ylim <ylim>).
        """

        plt.ylim(args)
    
    def do_yscale(self, args):
        """
        Changes the yscale (type yscale <yscale>).
        """

        plt.yscale(args)
    
    def do_savefig(self, args):
        """
        Save the plot into a file (type savefig <name>).
        """

        plt.savefig(args)
        click.echo("Image file saved at %s.png" %args)

    def do_quit(self, args):
        """
        Quits the interactive plotting window (type quit).
        """

        if(click.confirm("Are you sure you want to leave the plotting window?")):

            raise SystemExit
    
    def do_exit(self, args):
        """
        Exits the interactive plotting window (type exit).
        """

        if(click.confirm("Are you sure you want to leave the plotting window?")):

            raise SystemExit

# Global Variables

fmax = 0
fmin = 0
delta = 0
period = 0
frequency = 0
time = np.array([])
phase = np.array([])
periodogram = np.array([])
frequencies = np.array([])