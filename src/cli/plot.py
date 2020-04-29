#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries

import cmd
import click
import numpy as np
import matplotlib.pyplot as plt
from src.cli import globals
from src.file import text
from typing import List

# globalsal Objects


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

        axes = plt.gca().get_xlim()

        click.echo(axes)

        if(click.confirm("Do you want to calculate the Z2n statistics with the new limits?")):

            globals.fmin = axes[0]
            globals.fmax = axes[1]

            globals.delta = float(input("Frequency steps on the spectrum: "))

            globals.frequencies = np.arange(
                globals.fmin, globals.fmax, globals.delta)

            click.echo("Try run stats command for Z2n Statistics.")

            raise SystemExit

    def do_normal(self, args: None) -> None:
        """
        Adjust guassian distribution to peak value (type normal).
        """

        axes = plt.gca().get_xlim()

        click.echo(axes)

    def do_error(self, args: None) -> None:
        """
        Select the uncertainty forest (type error).
        """

        regions = int(input("How many regions of uncertainty? "))

        for k in range(regions):

            means = np.zeros(regions)

            if(click.confirm(f"Did you select the region {k+1}?")):

                axes = plt.gca().get_xlim()

                i = np.argwhere(np.isclose(globals.frequencies, axes[0], 0.1))

                j = np.argwhere(np.isclose(globals.frequencies, axes[1], 0.1))

                means[k] = np.mean(globals.periodogram[i[0][0] : j[0][0]])

        mean = np.mean(means)

        peak = np.max(globals.periodogram)

        globals.forest = mean
        click.echo(f"Uncertainty of the system: {globals.forest} Hz")

        globals.band = peak - mean
        click.echo(f"Bandwidth of the system: {globals.band} Hz")

    def do_back(self, args: str) -> None:
        """
        Adds subplot of the background (type back <string>).
        """

        if(args is None):
            args = input("Path to background file: ")

        globals.background = text.load_fits(args)

        plt.close()

        fig, ax = plt.subplots(2)

        ax[1].plot(globals.background, color='tab:blue')

        ax[0].plot(globals.frequencies, globals.periodogram, color='tab:blue',
                label=f"Z2n Statistics\nxmin: {globals.fmin:.4e}\n xmax: {globals.fmax:.4e}\n delta: {globals.delta:.4e}")

    def do_peak(self, args: None) -> None:
        """
        Adds vertical line to the peak value (type peak).
        """
        plt.axvline(globals.peak, color='tab:red',
                    label=f"peak: {globals.peak:.4e}")

    def do_band(self, args: None) -> None:
        """
        Adds horizontal line to the bandwidth value (type band).
        """
        plt.axhline(globals.band, color='tab:gray',
                    label=f"band: {globals.band:.4e}")

    def do_legend(self, args: None) -> None:
        """
        Adds legend to the figure (type legend).
        """
        plt.legend(loc='best')

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
