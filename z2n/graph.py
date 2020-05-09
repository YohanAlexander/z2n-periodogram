#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import numpy as np
import matplotlib.pyplot as plt

# Other Libraries
from z2n import series


class Graph(series.Series):
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

    def rm_background(self) -> None:
        self.plots = 1

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

    def get_regions(self) -> str:
        click.secho(f"{self.regions} regions of uncertainty", fg='cyan')
        return self.regions

    def set_regions(self) -> None:
        self.regions = click.prompt("How many regions", type=int)

    def plot_figure(self) -> int:
        plt.close()
        plt.ion()
        if self.plots == 1:
            self.figure, self.axes = plt.subplots(self.plots)
            self.axes.plot(self.data.bins, self.data.z2n)
            return 0
        elif self.plots == 2:
            self.figure, self.axes = plt.subplots(
                self.plots, sharex=True, sharey=True)
            self.axes[0].plot(self.data.bins, self.data.z2n)
            self.axes[1].plot(self.back.bins, self.back.z2n)
            return 0
        else:
            return 1

    def change_axis(self) -> None:
        self.axis = plt.gca().get_xlim()
        low = np.where(np.isclose(self.data.bins, self.axis[0], 0.1))
        up = np.where(np.isclose(self.data.bins, self.axis[1], 0.1))
        self.low = np.rint(np.median(low)).astype(int)
        self.up = np.rint(np.median(up)).astype(int)
        self.size = self.up - self.low

    def change_whole(self) -> None:
        if click.confirm("Are the new limits selected"):
            self.change_axis()
            self.data.fmin = self.axis[0]
            self.data.fmax = self.axis[1]
            self.data.set_delta()
            self.data.set_bins()
            self.data.set_periodogram()

    # Not working
    def change_region(self) -> None:
        if click.confirm("Is the region selected"):
            self.change_axis()
            self.set_bins()
            self.set_periodogram()
            total = (self.data.bins.size - self.size) + self.bins.size
            final = self.low + self.bins.size
            self.bins[:self.low] = self.data.bins[:self.low]
            self.z2n[:self.low] = self.data.z2n[:self.low]
            self.bins[self.low:final] = self.bins
            self.z2n[self.low:final] = self.z2n
            self.bins[final:] = self.data.bins[self.up:]
            self.z2n[final:] = self.data.z2n[self.up:]
            self.data.bins = self.bins
            self.data.z2n = self.z2n

    def recalculate_figure(self) -> None:
        if click.confirm("Drop the other bins"):
            self.change_whole()
        else:
            self.change_region()

    def change_forest(self) -> None:
        self.plot_figure()
        self.set_regions()
        means = np.zeros(self.regions)
        for region in range(self.regions):
            if click.confirm(f"Is the the region {region + 1} selected"):
                self.change_axis()
                means[region] = np.mean(self.data.z2n[self.low:self.up])
        self.data.forest = np.mean(means)

    def save_image(self) -> int:
        plt.tight_layout()
        self.set_output()
        self.set_format()
        if self.format == 'png':
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            return 0
        elif self.format == 'pdf':
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            return 0
        elif self.format == 'ps':
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            return 0
        elif self.format == 'eps':
            plt.savefig(f'{self.output}.{self.format}', format=self.format)
            return 0
        else:
            return 1

    def fit_gauss(self) -> None:
        pass
