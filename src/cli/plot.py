#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries

import cmd
import click
import numpy as np
import matplotlib.pyplot as plt
from src.cli import globals
from typing import List

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

            If you want to recalculate the spectrum with different axis,
            change the axis on the plotting window and type "axes".
            """

    def do_axes(self, args: None) -> None:
        """
        Get the current axes (type axes).
        """

        axes = plt.gca().get_xlim()

        click.echo(axes)

        if(click.confirm("Do you want to calculate the Z2n statistics with the new limits?")):

            globals.fmin = axes[0]
            globals.fmax = axes[1]

            globals.delta = float(input("Frequency steps on the spectrum: "))

            globals.frequencies = np.arange(globals.fmin, globals.fmax, globals.delta)

            click.echo("Try run stats command for Z2n Statistics.")

            raise SystemExit

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

        click.echo(f"Image file saved at {args}.png")

    def do_quit(self, args: None) -> None:
        """
        Quits the interactive plotting window (type quit).
        """

        if(click.confirm("Are you sure you want to leave the plotting window?")):

            raise SystemExit

    def do_exit(self, args: None) -> None:
        """
        Quits the interactive plotting window (type quit).
        """

        if(click.confirm("Are you sure you want to leave the plotting window?")):

            raise SystemExit
