#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
import numpy as np
import matplotlib.pyplot as plt

# Owned Libraries
from z2n import file
from z2n import stats
from z2n.series import Series


class Plot():
    """
    A class to represent the plot of a time series.

    Attributes
    ----------
    * `input : str`
    > A string that represents the input file path.
    * `output : str`
    > A string that represents the output file name.
    * `format : str`
    > A string that represents the file format.
    * `back : int`
    > A integer for the state of the background.
    * `data : Series`
    > A series object that represents the data.
    * `noise : Series`
    > A series object that represents the background.

    Methods
    -------
    """

    def __init__(self) -> None:
        self.input = ""
        self.output = ""
        self.format = ""
        self.back = 0
        self.data = Series()
        self.noise = Series()
        self.figure, self.axes = ((), ())

    def get_input(self) -> str:
        """Return the input image name."""
        click.secho(f"Path of the periodogram: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        """Change the input image name."""
        self.input = click.prompt(
            "Path of the periodogram", type=click.Path(exists=True))

    def get_output(self) -> str:
        """Return the output image name."""
        click.secho(f"Name of the image: {self.output}", fg='cyan')
        return self.output

    def set_output(self) -> None:
        """Change the output image name."""
        self.output = click.prompt("Name of the image")

    def get_format(self) -> str:
        """Return the image format."""
        click.secho(f"File format: {self.format}", fg='cyan')
        return self.format

    def set_format(self) -> None:
        """Change the image format."""
        self.format = click.prompt("Which format [png, pdf, ps, eps]")

    def add_background(self) -> None:
        """Add background on the plot."""
        self.back = 1
        click.secho("Background file added.", fg='green')

    def rm_background(self) -> None:
        """Remove background on the plot."""
        self.back = 0
        del self.noise
        self.noise = Series()
        click.secho("Background file removed.", fg='green')

    def plot_peak(self) -> None:
        """Add vertical line on the peak frequency."""
        if click.confirm("Add a vertical line to the peak frequency"):
            if not self.back:
                self.axes.axvline(
                    self.data.frequency, linestyle='dashed', color='tab:red')
            else:
                self.axes[0].axvline(
                    self.data.frequency, linestyle='dashed', color='tab:red')
            click.secho("Peak line added.", fg='green')

    def plot_figure(self) -> None:
        """Create the figure on the plotting window."""
        plt.close()
        plt.ion()
        if not self.back:
            self.figure, self.axes = plt.subplots(self.back + 1)
            self.axes.plot(self.data.bins, self.data.z2n, color='tab:blue')
        else:
            self.figure, self.axes = plt.subplots(
                self.back + 1, sharex=True, sharey=True)
            self.axes[0].plot(self.data.bins, self.data.z2n, color='tab:blue')
            self.axes[1].plot(
                self.noise.bins, self.noise.z2n, color='tab:cyan')

    def plot_file(self) -> int:
        """Plot the periodogram from a file."""
        flag = 0
        click.secho("The periodogram file is needed.", fg='yellow')
        self.data.set_format()
        if self.data.format == 'ascii':
            self.data.set_input()
            file.plot_ascii(self.data)
            click.secho("Periodogram loaded.", fg='green')
            self.plot_figure()
            stats.error(self.data)
            self.plot_figure()
            self.data.get_parameters()
        elif self.data.format == 'csv':
            self.data.set_input()
            file.plot_csv(self.data)
            click.secho("Periodogram loaded.", fg='green')
            self.plot_figure()
            stats.error(self.data)
            self.plot_figure()
            self.data.get_parameters()
        elif self.data.format == 'fits':
            self.data.set_input()
            file.plot_fits(self.data)
            click.secho("Periodogram loaded.", fg='green')
            self.plot_figure()
            stats.error(self.data)
            self.plot_figure()
            self.data.get_parameters()
        elif self.data.format == 'hdf5':
            self.data.set_input()
            file.plot_hdf5(self.data)
            click.secho("Periodogram loaded.", fg='green')
            self.plot_figure()
            stats.error(self.data)
            self.plot_figure()
            self.data.get_parameters()
        else:
            click.secho(
                f"{self.data.format} format not supported.", fg='red')
            flag = 1
        return flag

    def plot_background(self) -> int:
        """Create subplot of the background."""
        flag = 0
        click.secho("The background file is needed.", fg='yellow')
        if not self.noise.set_time():
            self.noise.bins = np.array(self.data.bins)
            plt.close()
            self.noise.set_periodogram()
            self.add_background()
            self.plot_figure()
        else:
            flag = 1
        return flag

    def plot_periodogram(self) -> int:
        """Create plot of the periodogram."""
        flag = 0
        if not self.data.z2n.size:
            click.secho("The time series file is needed.", fg='yellow')
            if not self.data.set_time():
                if not self.data.set_bins():
                    plt.close()
                    self.data.set_periodogram()
                    self.plot_figure()
                    self.data.set_parameters()
                    self.plot_figure()
                    self.data.get_parameters()
                    if click.confirm("Do you want to add a background file"):
                        self.plot_background()
                else:
                    flag = 1
            else:
                flag = 1
        else:
            if click.confirm("Do you want to recalculate on a selected region"):
                click.secho(
                    "This will recalculate the periodogram.", fg='yellow')
                self.rm_background()
                self.plot_figure()
                flag2 = 1
                while flag2:
                    if click.confirm("Is the region selected"):
                        axis = plt.gca().get_xlim()
                        self.data.fmin = axis[0]
                        self.data.fmax = axis[1]
                        if not self.data.set_bins():
                            plt.close()
                            self.data.set_periodogram()
                            self.plot_figure()
                            self.data.set_parameters()
                            self.plot_figure()
                            self.data.get_parameters()
                            if click.confirm("Do you want to add a background file"):
                                self.plot_background()
                            flag = 0
                            flag2 = 0
                        else:
                            flag = 1
                            flag2 = 0
                    else:
                        flag = 1
            else:
                flag = 1
        return flag

    def save_image(self) -> None:
        """Save the image on a file."""
        plt.tight_layout()
        self.set_format()
        if self.format == 'png':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'pdf':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'ps':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'eps':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        else:
            click.secho(f"{self.format} format not supported.", fg='red')

    def change_title(self) -> None:
        """Change the title on the figure."""
        if self.back:
            self.figure.suptitle(click.prompt("Which title"))
            click.secho("Changed title.", fg='green')
        else:
            self.axes.set_title(click.prompt("Which title"))
            click.secho("Changed title.", fg='green')

    def change_xlabel(self) -> None:
        """Change the label on the x axis."""
        if self.back:
            xlabel = click.prompt("Which label")
            self.axes[0].set_xlabel(xlabel)
            self.axes[1].set_xlabel(xlabel)
            click.secho("Changed X axis label.", fg='green')
        else:
            self.axes.set_xlabel(click.prompt("Which label"))
            click.secho("Changed X axis label.", fg='green')

    def change_xscale(self) -> None:
        """Change the scale on the x axis."""
        if self.back:
            self.axes[0].set_xscale(click.prompt(
                "Which scale [linear, log]"))
            click.secho("Changed X axis scale.", fg='green')
        else:
            self.axes.set_xscale(click.prompt(
                "Which scale [linear, log]"))
            click.secho("Changed X axis scale.", fg='green')

    def change_xlim(self) -> None:
        """Change the limites on the x axis."""
        if self.back:
            low = click.prompt("Which lower limit", type=float)
            up = click.prompt("Which upper limit", type=float)
            self.axes[0].set_xlim([low, up])
            click.secho("Changed X axis limits.", fg='green')
        else:
            low = click.prompt("Which lower limit", type=float)
            up = click.prompt("Which upper limit", type=float)
            self.axes.set_xlim([low, up])
            click.secho("Changed X axis limits.", fg='green')

    def change_ylabel(self) -> None:
        """Change the label on the y axis."""
        if self.back:
            ylabel = click.prompt("Which label")
            self.axes[0].set_ylabel(ylabel)
            self.axes[1].set_ylabel(ylabel)
            click.secho("Changed y axis label.", fg='green')
        else:
            self.axes.set_ylabel(click.prompt("Which label"))
            click.secho("Changed y axis label.", fg='green')

    def change_yscale(self) -> None:
        """Change the scale on the y axis."""
        if self.back:
            self.axes[0].set_yscale(click.prompt(
                "Which scale [linear, log]"))
            click.secho("Changed y axis scale.", fg='green')
        else:
            self.axes.set_yscale(click.prompt(
                "Which scale [linear, log]"))
            click.secho("Changed y axis scale.", fg='green')

    def change_ylim(self) -> None:
        """Change the limites on the y axis."""
        if self.back:
            low = click.prompt("Which lower limit", type=float)
            up = click.prompt("Which upper limit", type=float)
            self.axes[0].set_ylim([low, up])
            click.secho("Changed y axis limits.", fg='green')
        else:
            low = click.prompt("Which lower limit", type=float)
            up = click.prompt("Which upper limit", type=float)
            self.axes.set_ylim([low, up])
            click.secho("Changed y axis limits.", fg='green')
