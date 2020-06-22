#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
import pathlib
import numpy as np
import matplotlib.pyplot as plt

# Owned Libraries
from z2n import stats
from z2n.series import Series


class Plot:
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
        self.back = 0
        self.input = ""
        self.output = ""
        self.format = ""
        self.data = Series()
        self.noise = Series()
        self.figure, self.axes = ((), ())

    def get_input(self) -> str:
        """Return the input image name."""
        click.secho(f"Path of the periodogram: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        """Change the input image name."""
        self.input = click.prompt("Filename", type=click.Path(exists=True))

    def get_output(self) -> str:
        """Return the output image name."""
        click.secho(f"Name of the image: {self.output}", fg='cyan')
        return self.output

    def set_output(self) -> None:
        """Change the output image name."""
        default = "z2n_" + pathlib.Path(self.data.input).stem
        flag = 1
        while flag:
            self.output = click.prompt(
                "Name of the image", default, type=click.Path())
            if pathlib.Path(f"{self.output}.{self.format}").is_file():
                click.secho("File already exists.", fg='red')
            else:
                flag = 0

    def get_format(self) -> str:
        """Return the image format."""
        click.secho(f"File format: {self.format}", fg='cyan')
        return self.format

    def set_format(self) -> None:
        """Change the image format."""
        self.format = click.prompt(
            "Format", "ps", type=click.Choice(['png', 'pdf', 'ps', 'eps']))

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

    def plot_figure(self) -> None:
        """Create the figure on the plotting window."""
        plt.close()
        plt.ion()
        if not self.back:
            self.figure, self.axes = plt.subplots(self.back + 1)
            self.axes.plot(
                self.data.bins, self.data.z2n, label='Z2n Power',
                color='tab:blue', linewidth=2)
            self.axes.plot(
                self.data.gauss.bins, self.data.gauss.z2n,
                color='tab:red', label='Gaussian Fit', linewidth=1)
            self.axes.set_xlabel('Frequency (Hz)')
            self.axes.set_ylabel('Power')
            self.axes.legend(loc='best')
        else:
            self.figure, self.axes = plt.subplots(
                self.back + 1, sharex=True, sharey=True)
            self.axes[0].plot(
                self.data.bins, self.data.z2n, label='Z2n Power',
                color='tab:blue', linewidth=2)
            self.axes[0].plot(
                self.data.gauss.bins, self.data.gauss.z2n,
                color='tab:red', label='Gaussian Fit', linewidth=1)
            self.axes[1].plot(
                self.noise.bins, self.noise.z2n, color='tab:cyan',
                label='Background')
            self.axes[0].set_xlabel('Frequency (Hz)')
            self.axes[0].set_ylabel('Power')
            self.axes[1].set_xlabel('Frequency (Hz)')
            self.axes[1].set_ylabel('Power')
            self.axes[0].legend(loc='best')
            self.axes[1].legend(loc='best')
        plt.tight_layout()

    def plot_background(self) -> int:
        """Create subplot of the background."""
        flag = 0
        click.secho("The background file is needed.", fg='yellow')
        if not self.noise.set_time():
            self.noise.bins = np.array(self.data.bins)
            self.noise.harmonics = self.data.harmonics
            plt.close()
            self.noise.z2n = np.zeros(self.noise.bins.size)
            stats.periodogram(self.noise)
            self.add_background()
            self.plot_figure()
        else:
            flag = 1
        return flag

    def plot_periodogram(self) -> int:
        """Create plot of the periodogram."""
        flag = 0
        if not self.data.z2n.size:
            click.secho("The event file is needed.", fg='yellow')
            if not self.data.set_time():
                if not self.data.set_bins():
                    plt.close()
                    self.data.set_periodogram()
                    self.data.plot()
                    self.plot_figure()
                    self.save_image()
                    if click.confirm("Add a background file", prompt_suffix='? '):
                        self.plot_background()
                else:
                    flag = 1
            else:
                flag = 1
        else:
            opt = click.prompt(
                "Use another file [1] or recalculate [2]", type=int)
            if opt in (1, 2):
                self.rm_background()
                if opt == 1:
                    del self.data
                    self.data = Series()
                    self.plot_periodogram()
                    flag = 1
                elif opt == 2:
                    click.secho(
                        "This will recalculate the periodogram.", fg='yellow')
                    self.plot_figure()
                    flag2 = 1
                    while flag2:
                        if click.confirm("Is the region selected", prompt_suffix='? '):
                            axis = plt.gca().get_xlim()
                            self.data.fmin = axis[0]
                            self.data.fmax = axis[1]
                            if not self.data.set_bins():
                                plt.close()
                                self.data.set_periodogram()
                                self.data.plot()
                                self.plot_figure()
                                self.save_image()
                                if click.confirm(
                                        "Add a background file", prompt_suffix='? '):
                                    self.plot_background()
                                flag = 0
                                flag2 = 0
                            else:
                                flag = 1
                                flag2 = 0
            else:
                flag = 1
                click.secho("Select '1' or '2'.", fg='red')
        return flag

    def save_image(self) -> None:
        """Save the image on a file."""
        plt.tight_layout()
        click.secho("Save the periodogram on a image.", fg='yellow')
        self.set_format()
        if self.format == 'png':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(
                f"Image saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'pdf':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(
                f"Image saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'ps':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(
                f"Image saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'eps':
            self.set_output()
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            click.secho(
                f"Image saved at {self.output}.{self.format}", fg='green')
        else:
            click.secho(f"{self.format} format not supported.", fg='red')

    def change_title(self) -> None:
        """Change the title on the figure."""
        if self.back:
            self.figure.suptitle(click.prompt(
                "Which title", "Z2n Periodogram"))
            click.secho("Changed title.", fg='green')
        else:
            self.axes.set_title(click.prompt("Which title", "Z2n Periodogram"))
            click.secho("Changed title.", fg='green')

    def change_xlabel(self) -> None:
        """Change the label on the x axis."""
        if self.back:
            xlabel = click.prompt("Which label", "Frequency (Hz)")
            self.axes[0].set_xlabel(xlabel)
            self.axes[1].set_xlabel(xlabel)
            click.secho("Changed X axis label.", fg='green')
        else:
            self.axes.set_xlabel(click.prompt("Which label", "Frequency (Hz)"))
            click.secho("Changed X axis label.", fg='green')

    def change_xscale(self) -> None:
        """Change the scale on the x axis."""
        if self.back:
            self.axes[0].set_xscale(click.prompt(
                "Which scale [linear, log]", "linear"))
            click.secho("Changed X axis scale.", fg='green')
        else:
            self.axes.set_xscale(click.prompt(
                "Which scale [linear, log]", "linear"))
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
            ylabel = click.prompt("Which label", "Power")
            self.axes[0].set_ylabel(ylabel)
            self.axes[1].set_ylabel(ylabel)
            click.secho("Changed y axis label.", fg='green')
        else:
            self.axes.set_ylabel(click.prompt("Which label", "Power"))
            click.secho("Changed y axis label.", fg='green')

    def change_yscale(self) -> None:
        """Change the scale on the y axis."""
        if self.back:
            self.axes[0].set_yscale(click.prompt(
                "Which scale [linear, log]", "linear"))
            click.secho("Changed y axis scale.", fg='green')
        else:
            self.axes.set_yscale(click.prompt(
                "Which scale [linear, log]", "linear"))
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
