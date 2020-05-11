#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt

# Other Libraries
from z2n import series


class Plot(series.Series):
    """
    A class to represent the plot of a time series.
    ...

    Attributes
    ----------
    plots : int
        A integer for the current number of plots.

    Methods
    -------
    ...
    """

    def __init__(self, data, back) -> None:
        super().__init__()
        self.plots = 1
        self.data = data
        self.back = back
        self.figure, self.axes = plt.subplots()
        self.axis = plt.gca().get_xlim()
        self.low = 0
        self.up = 0
        self.size = 0
        self.regions = 0

    def add_background(self) -> None:
        self.plots = 2
        click.secho("Background file added.", fg='green')

    def rm_background(self) -> None:
        self.plots = 1
        click.secho("Background file removed.", fg='green')

    def get_output(self) -> str:
        click.secho(f"Name of the image: {self.output}", fg='cyan')
        return self.output

    def set_output(self) -> None:
        self.output = click.prompt("Name of the image")

    def get_format(self) -> str:
        click.secho(f"File format: {self.format}", fg='cyan')
        return self.format

    def set_format(self) -> None:
        self.format = click.prompt("Which format [png, pdf, ps, eps]")

    def get_regions(self) -> int:
        click.secho(f"{self.regions} regions of uncertainty", fg='cyan')
        return self.regions

    def set_regions(self) -> None:
        self.regions = click.prompt("How many regions", type=int)

    def add_peak(self) -> None:
        if self.plots == 1:
            self.axes.axvline(self.data.peak, color='tab:red')
        else:
            self.axes[0].axvline(self.data.peak, color='tab:red')
        click.secho("Peak line added.", fg='green')

    def add_band(self) -> None:
        if self.plots == 1:
            self.axes.axhline(self.data.band, color='tab:gray')
        else:
            self.axes[0].axhline(self.data.band, color='tab:gray')
        click.secho("Bandwidth line added.", fg='green')

    def add_lines(self) -> None:
        self.data.set_frequency()
        self.data.set_band()
        if click.confirm("Add a vertical line to the peak frequency"):
            self.add_peak()
        if click.confirm("Add a horizontal line to the bandwidth"):
            self.add_band()

    def plot_periodogram(self) -> None:
        if click.confirm("Do you want to plot from a file"):
            if not self.data.get_z2n():
                self.plot_figure()

    def plot_figure(self) -> None:
        plt.close()
        plt.ion()
        if self.plots == 1:
            self.figure, self.axes = plt.subplots(self.plots)
            self.axes.plot(self.data.bins, self.data.z2n)
        elif self.plots == 2:
            self.figure, self.axes = plt.subplots(
                self.plots, sharex=True, sharey=True)
            self.axes[0].plot(self.data.bins, self.data.z2n)
            self.axes[1].plot(self.back.bins, self.back.z2n)

    def plot_background(self) -> None:
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

    def change_axis(self) -> None:
        self.axis = plt.gca().get_xlim()
        low = np.where(np.isclose(self.data.bins, self.axis[0], 0.1))
        up = np.where(np.isclose(self.data.bins, self.axis[1], 0.1))
        self.low = np.rint(np.median(low)).astype(int)
        self.up = np.rint(np.median(up)).astype(int)
        self.size = self.up - self.low

    def change_whole(self) -> None:
        click.secho("This will recalculate the periodogram.", fg='yellow')
        self.plot_figure()
        if click.confirm("Are the new limits selected"):
            self.change_axis()
            self.data.fmin = self.axis[0]
            self.data.fmax = self.axis[1]
            self.data.set_delta()
            self.data.bins = np.arange(self.fmin, self.fmax, self.delta)
            self.data.set_periodogram()

    def change_region(self) -> None:
        click.secho("This will recalculate the periodogram.", fg='yellow')
        self.plot_figure()
        if click.confirm("Is the region selected"):
            self.change_axis()
            self.fmin = self.axis[0]
            self.fmax = self.axis[1]
            self.set_delta()
            self.bins = np.arange(self.fmin, self.fmax, self.delta)
            self.time = self.data.time
            self.set_periodogram()
            size = (self.data.bins.size - self.size) + self.bins.size
            middle = self.low + self.bins.size
            tempx = np.zeros(size)
            tempy = np.zeros(size)
            tempx[:self.low] = self.data.bins[:self.low]
            tempy[:self.low] = self.data.z2n[:self.low]
            tempx[self.low:middle] = self.bins
            tempy[self.low:middle] = self.z2n
            tempx[middle:] = self.data.bins[self.up:]
            tempy[middle:] = self.data.z2n[self.up:]
            self.data.bins = tempx
            self.data.z2n = tempy

    def recalculate_figure(self) -> None:
        if click.confirm("Recalculate with different limits"):
            if click.confirm("Drop the other bins"):
                self.change_whole()
                if self.plots == 2:
                    self.back.bins = self.data.bins
                    self.back.set_periodogram()
            else:
                self.change_region()

    def change_forest(self) -> None:
        click.secho("Select regions to estimate error.", fg='yellow')
        self.plot_figure()
        self.set_regions()
        if self.regions > 0:
            means = np.zeros(self.regions)
            for region in range(self.regions):
                if click.confirm(f"Is the the region {region + 1} selected"):
                    self.change_axis()
                    means[region] = np.mean(self.data.z2n[self.low:self.up])
            self.data.forest = np.mean(means)
            self.set_band()
        else:
            click.secho("No regions to estimate error.", fg='yellow')

    def save_image(self) -> None:
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
        if self.plots != 1:
            self.figure.suptitle(click.prompt("Which title"))
            click.secho("Changed title.", fg='green')
        else:
            self.axes.set_title(click.prompt("Which title"))
            click.secho("Changed title.", fg='green')

    def change_xlabel(self) -> None:
        if self.plots != 1:
            xlabel = click.prompt("Which label")
            self.axes[0].set_xlabel(xlabel)
            self.axes[1].set_xlabel(xlabel)
            click.secho("Changed X axis label.", fg='green')
        else:
            self.axes.set_xlabel(click.prompt("Which label"))
            click.secho("Changed X axis label.", fg='green')

    def change_xscale(self) -> None:
        if self.plots != 1:
            self.axes[0].set_xscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed X axis scale.", fg='green')
        else:
            self.axes.set_xscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed X axis scale.", fg='green')

    def change_xlim(self) -> None:
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
        if self.plots != 1:
            ylabel = click.prompt("Which label")
            self.axes[0].set_ylabel(ylabel)
            self.axes[1].set_ylabel(ylabel)
            click.secho("Changed y axis label.", fg='green')
        else:
            self.axes.set_ylabel(click.prompt("Which label"))
            click.secho("Changed y axis label.", fg='green')

    def change_yscale(self) -> None:
        if self.plots != 1:
            self.axes[0].set_yscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed y axis scale.", fg='green')
        else:
            self.axes.set_yscale(click.prompt(
                "Which scale [linear, log, symlog, logit]"))
            click.secho("Changed y axis scale.", fg='green')

    def change_ylim(self) -> None:
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

    def fit_gauss(self) -> None:
        pass

    def plot_z2n(self) -> None:
        if self.data.input != "":
            if click.confirm("Do you want to use another file"):
                if not self.data.load_file():
                    if not self.data.set_z2n():
                        if self.plots == 2:
                            self.back.bins = self.data.bins
                            self.back.set_periodogram()
                        self.change_forest()
            else:
                if self.data.time.size:
                    if not self.recalculate_figure():
                        self.change_forest()
                else:
                    click.secho("No time series set.", fg='red')
        else:
            if not self.data.load_file():
                if not self.data.set_z2n():
                    self.change_forest()
