#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
import numpy as np
import matplotlib.pyplot as plt

# Owned Libraries
from z2n import series


class Plot(series.Series):
    """
    A class to represent the plot of a time series.

    Attributes
    ----------
    * `plots : int`
    > A integer for the current number of plots.
    * `data : Series`
    > A series object that represents the data.
    * `back : Series`
    > A series object that represents the background.

    Methods
    -------
    """

    def __init__(self, data, back) -> None:
        super().__init__()
        self.plots = 1
        self.data = data
        self.back = back
        self.figure, self.axes = plt.subplots()
        self.axis = plt.gca().get_xlim()

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
        self.plots = 2
        click.secho("Background file added.", fg='green')

    def rm_background(self) -> None:
        """Remove background on the plot."""
        self.plots = 1
        click.secho("Background file removed.", fg='green')

    def add_peak(self) -> None:
        """Add vertical line on the peak frequency."""
        if click.confirm("Add a vertical line to the peak frequency"):
            if self.plots == 1:
                self.axes.axvline(
                    self.data.frequency, linestyle='dashed', color='tab:red')
            else:
                self.axes[0].axvline(
                    self.data.frequency, linestyle='dashed', color='tab:red')
            click.secho("Peak line added.", fg='green')

    def add_band(self) -> None:
        """Add horizontal line on the bandwidth."""
        if click.confirm("Add a horizontal line to the bandwidth"):
            if self.plots == 1:
                self.axes.axhline(
                    self.data.bandwidth, linestyle='dotted', color='tab:grey')
            else:
                self.axes[0].axhline(
                    self.data.bandwidth, linestyle='dotted', color='tab:grey')
            click.secho("Bandwidth line added.", fg='green')

    def plot_figure(self) -> None:
        """Create the figure on the plotting window."""
        plt.close()
        plt.ion()
        if self.plots == 1:
            self.figure, self.axes = plt.subplots(self.plots)
            self.axes.plot(self.data.bins, self.data.z2n, color='tab:blue')
        elif self.plots == 2:
            self.figure, self.axes = plt.subplots(
                self.plots, sharex=True, sharey=True)
            self.axes[0].plot(self.data.bins, self.data.z2n, color='tab:blue')
            self.axes[1].plot(self.back.bins, self.back.z2n, color='tab:cyan')

    def plot_background(self) -> None:
        """Create subplot of the background."""
        self.back.bins = self.data.bins
        if self.plots == 2:
            opt = click.prompt("Change the background [1] or remove it [2]")
            if opt == '1':
                if not self.back.load_file():
                    self.back.set_periodogram()
                    self.add_background()
                    self.plot_figure()
            elif opt == '2':
                self.rm_background()
                self.plot_figure()
            else:
                click.secho("Select '1' or '2'.", fg='red')
        else:
            if not self.back.load_file():
                self.back.set_periodogram()
                self.add_background()
                self.plot_figure()

    def plot_periodogram(self) -> None:
        """Create plot of the periodogram."""
        if self.data.z2n.size:
            if click.confirm("Do you want to use another file"):
                if not self.data.load_file():
                    if not self.data.save_periodogram():
                        if self.plots == 2:
                            self.back.bins = self.data.bins
                            self.back.set_periodogram()
                        self.change_forest()
                        self.data.get_parameters()
            else:
                if click.confirm("Recalculate with different limits"):
                    if click.confirm("Drop the other bins"):
                        self.change_whole()
                        if self.plots == 2:
                            self.back.bins = self.data.bins
                            self.back.set_periodogram()
                        self.change_forest()
                        self.data.get_parameters()
                    else:
                        self.change_region()
                        self.change_forest()
                        self.data.get_parameters()
        else:
            if not self.data.load_file():
                if not self.data.save_periodogram():
                    self.change_forest()
                    self.data.get_parameters()

    def change_whole(self) -> None:
        """Change limits on the whole periodogram."""
        click.secho("This will recalculate the periodogram.", fg='yellow')
        self.plot_figure()
        if click.confirm("Are the new limits selected"):
            self.axis = plt.gca().get_xlim()
            self.data.fmin = self.axis[0]
            self.data.fmax = self.axis[1]
            self.data.set_delta()
            self.data.bins = np.arange(self.fmin, self.fmax, self.delta)
            self.data.set_periodogram()

    def change_region(self) -> None:
        """Change limits on a periodogram region."""
        click.secho("This will recalculate the periodogram.", fg='yellow')
        self.plot_figure()
        if click.confirm("Is the region selected"):
            self.axis = plt.gca().get_xlim()
            lower = np.where(np.isclose(self.data.bins, self.axis[0], 0.1))
            upper = np.where(np.isclose(self.data.bins, self.axis[1], 0.1))
            low = np.rint(np.median(lower)).astype(int)
            up = np.rint(np.median(upper)).astype(int)
            self.fmin = self.axis[0]
            self.fmax = self.axis[1]
            self.set_delta()
            self.bins = np.arange(self.fmin, self.fmax, self.delta)
            self.time = self.data.time
            self.set_periodogram()
            size = (self.data.bins.size - (up - low)) + self.bins.size
            middle = low + self.bins.size
            tempx = np.zeros(size)
            tempy = np.zeros(size)
            tempx[:low] = self.data.bins[:low]
            tempy[:low] = self.data.z2n[:low]
            tempx[low:middle] = self.bins
            tempy[low:middle] = self.z2n
            tempx[middle:] = self.data.bins[up:]
            tempy[middle:] = self.data.z2n[up:]
            self.data.bins = tempx
            self.data.z2n = tempy

    def change_forest(self) -> None:
        """Select regions of uncertainty."""
        click.secho("Select regions to estimate error.", fg='yellow')
        self.plot_figure()
        regions = click.prompt("How many regions", type=int)
        if regions > 0:
            means = np.zeros(regions)
            for region in range(regions):
                if click.confirm(f"Is the the region {region + 1} selected"):
                    self.axis = plt.gca().get_xlim()
                    lower = np.where(np.isclose(
                        self.data.bins, self.axis[0], 0.1))
                    upper = np.where(np.isclose(
                        self.data.bins, self.axis[1], 0.1))
                    low = np.rint(np.median(lower)).astype(int)
                    up = np.rint(np.median(upper)).astype(int)
                    means[region] = np.mean(self.data.z2n[low:up])
            self.data.forest = np.mean(means)
            self.data.set_bandwidth()
        else:
            click.secho("No regions to estimate error.", fg='yellow')

    def save_image(self) -> None:
        """Save the image to a file."""
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
        if self.plots != 1:
            self.figure.suptitle(click.prompt("Which title"))
            click.secho("Changed title.", fg='green')
        else:
            self.axes.set_title(click.prompt("Which title"))
            click.secho("Changed title.", fg='green')

    def change_xlabel(self) -> None:
        """Change the label on the x axis."""
        if self.plots != 1:
            xlabel = click.prompt("Which label")
            self.axes[0].set_xlabel(xlabel)
            self.axes[1].set_xlabel(xlabel)
            click.secho("Changed X axis label.", fg='green')
        else:
            self.axes.set_xlabel(click.prompt("Which label"))
            click.secho("Changed X axis label.", fg='green')

    def change_xscale(self) -> None:
        """Change the scale on the x axis."""
        if self.plots != 1:
            self.axes[0].set_xscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed X axis scale.", fg='green')
        else:
            self.axes.set_xscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed X axis scale.", fg='green')

    def change_xlim(self) -> None:
        """Change the limites on the x axis."""
        if self.plots != 1:
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
        if self.plots != 1:
            ylabel = click.prompt("Which label")
            self.axes[0].set_ylabel(ylabel)
            self.axes[1].set_ylabel(ylabel)
            click.secho("Changed y axis label.", fg='green')
        else:
            self.axes.set_ylabel(click.prompt("Which label"))
            click.secho("Changed y axis label.", fg='green')

    def change_yscale(self) -> None:
        """Change the scale on the y axis."""
        if self.plots != 1:
            self.axes[0].set_yscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed y axis scale.", fg='green')
        else:
            self.axes.set_yscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed y axis scale.", fg='green')

    def change_ylim(self) -> None:
        """Change the limites on the y axis."""
        if self.plots != 1:
            low = click.prompt("Which lower limit", type=float)
            up = click.prompt("Which upper limit", type=float)
            self.axes[0].set_ylim([low, up])
            click.secho("Changed y axis limits.", fg='green')
        else:
            low = click.prompt("Which lower limit", type=float)
            up = click.prompt("Which upper limit", type=float)
            self.axes.set_ylim([low, up])
            click.secho("Changed y axis limits.", fg='green')
