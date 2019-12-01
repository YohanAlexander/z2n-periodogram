#! /usr/bin/python
# -*- coding: utf-8 -*-

# Wrapping Header

__author__ = 'Yohan Alexander'
__version__ = '0.4.0'
__copyright__ = 'Copyright (C) 2019, Z2n Software, by Yohan Alexander.'
__credits__ = ['''The Z2n Software was developed by Yohan Alexander as part of an undergradute research project, funded by the CNPq Institution, and it is supported by the Open Source community.''']
__license__ = 'MIT LICENSE'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'
__url__ = "https://z2n-periodogram.readthedocs.io"

__intro__ = f"""
        Z2n Software ({__version__}), a python package for optimized periodograms.
        Copyright (C) 2019, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.

        If you wish to run the software with the default values type "auto".
        """

# Generic/Built-in

import time, sys, os, functools, webbrowser

# Other Libraries

import cmd
import click
import prompt
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# Global Variables

peak = 0
fmax = 0
fmin = 0
delta = 0
period = 0
frequency = 0
time = np.array([])
phase = np.array([])
periodogram = np.array([])
frequencies = np.array([])

# Global Objects
class Plot(cmd.Cmd):
    """
    A class used to create the plotting cli.

    ...

    Attributes
    ----------
    prompt : str
        A formatted string to prompt on the cli.
    intro : str
        A formatted string to intro on the cli.

    Methods
    -------
    
    ...

    """
    
    prompt = '(plt) >>>'
    intro = """
            Interactive plotting window of the Z2n Software.
            Type "help" for more information.
            """

    def do_axes(self, args: None) -> None:
        """
        Get the current axes (type axes).
        """

        click.echo(plt.axes().get_xlim())

    def do_grid(self, args: bool) -> None:
        """
        Plots grid on the figure (type grid <bool>).
        """

        plt.grid(args)

    def do_title(self, args: str) -> None:
        """
        Changes the title (type title <string>).
        """

        plt.title(args)

    def do_xlabel(self, args: str) -> None:
        """
        Changes the xlabel (type xlabel <string>).
        """

        plt.xlabel(args)

    def do_xscale(self, args: str) -> None:
        """
        Changes the xscale (type xscale <"linear", "log", "symlog", "logit">).
        """

        plt.xscale(args)

    def do_xlim(self, args: List[float]) -> None:
        """
        Changes the xlim (type xlim <lower, upper>).
        """

        plt.xlim(list(args.split(',')))

    def do_ylabel(self, args: str) -> None:
        """
        Changes the ylabel (type ylabel <string>).
        """

        plt.ylabel(args)

    def do_yscale(self, args: str) -> None:
        """
        Changes the yscale (type yscale <"linear", "log", "symlog", "logit">).
        """

        plt.yscale(args)

    def do_ylim(self, args: List[float]) -> None:
        """
        Changes the ylim (type ylim <lower, upper>).
        """

        plt.ylim(list(args.split(',')))
    
    def do_savefig(self, args: str) -> None:
        """
        Save the plot into a file (type savefig <string>).
        """

        plt.savefig(args)

    def do_quit(self, args: None) -> None:
        """
        Quits the interactive plotting window (type quit).
        """

        if(click.confirm("Are you sure you want to leave the plotting window?")):

            raise SystemExit
    
    def do_exit(self, args: None) -> None:
        """
        Exits the interactive plotting window (type exit).
        """

        if(click.confirm("Are you sure you want to leave the plotting window?")):

            raise SystemExit
