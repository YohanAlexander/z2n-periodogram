#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import h5py
import click
import psutil
import numpy as np
import matplotlib.pyplot as plt

# Owned Libraries
from z2n import file
from z2n import stats
from z2n.series import Series


class Plot(Series):
    """
    A class to represent the plot of a time series.

    Attributes
    ----------
    * `plots : int`
    > A integer for the current number of plots.
    * `data : Series`
    > A series object that represents the data.
    * `noise : Series`
    > A series object that represents the background.

    Methods
    -------
    """

    def __init__(self) -> None:
        super().__init__()
        self.plots = 1
        self.data = Series()
        self.noise = Series()
        self.figure, self.axes = plt.subplots()

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
        self.plots = 2
        click.secho("Background file added.", fg='green')

    def rm_background(self) -> None:
        """Remove background on the plot."""
        self.plots = 1
        click.secho("Background file removed.", fg='green')

    def plot_frequency(self) -> None:
        """Add vertical line on the peak frequency."""
        if click.confirm("Add a vertical line to the peak frequency"):
            self.data.set_frequency()
            if self.plots == 1:
                self.axes.axvline(
                    self.data.frequency, linestyle='dashed', color='tab:red')
            else:
                self.axes[0].axvline(
                    self.data.frequency, linestyle='dashed', color='tab:red')
            click.secho("Peak line added.", fg='green')

    def plot_bandwidth(self) -> None:
        """Add horizontal line on the bandwidth."""
        if click.confirm("Add a horizontal line to the bandwidth"):
            self.data.set_bandwidth()
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
            self.axes[1].plot(self.noise.bins, self.noise.z2n, color='tab:cyan')

    def plot_file(self) -> int:
        """Plot the periodogram from a file."""
        flag = 0
        click.secho("The time series file is needed.", fg='yellow')
        if not self.data.set_time():
            click.secho("The periodogram file is needed.", fg='yellow')
            self.data.set_format()
            if self.data.format == 'ascii':
                self.set_input()
                self.data.input = self.input
                file.plot_ascii(self.data)
                click.secho("File loaded.", fg='green')
                self.plot_figure()
            elif self.data.format == 'csv':
                self.set_input()
                self.data.input = self.input
                file.plot_csv(self.data)
                click.secho("File loaded.", fg='green')
                self.plot_figure()
            elif self.data.format == 'fits':
                self.set_input()
                self.data.input = self.input
                file.plot_fits(self.data)
                click.secho("File loaded.", fg='green')
                self.plot_figure()
            elif self.data.format == 'hdf5':
                self.set_input()
                self.data.input = self.input
                file.plot_hdf5(self.data)
                click.secho("File loaded.", fg='green')
                self.plot_figure()
            else:
                click.secho(
                    f"{self.data.format} format not supported.", fg='red')
                flag = 1
        else:
            flag = 1
        return flag

    def plot_background(self) -> int:
        """Create subplot of the background."""
        flag = 0
        click.secho("The background file is needed.", fg='yellow')
        if not self.noise.set_time():
            try:
                self.noise.bins = np.array(self.data.bins)
                plt.close()
                self.noise.set_periodogram()
                self.add_background()
                self.plot_figure()
            except KeyboardInterrupt:
                click.secho(
                    "Error calculating the periodogram.", fg='red')
                self.rm_background()
                flag = 1
        else:
            flag = 1
        return flag

    def plot_periodogram(self) -> int:
        """Create plot of the periodogram."""
        flag = 0
        if self.data.z2n.size:
            if click.confirm("Recalculate on a selected region"):
                if not self.crop_region():
                    if self.plots == 2:
                        if click.confirm("Do you want to keep the background"):
                            try:
                                self.noise.bins = np.array(self.data.bins)
                                plt.close()
                                self.noise.set_periodogram()
                                self.plot_figure()
                                self.data.set_parameters()
                                self.plot_figure()
                                self.data.get_parameters()
                            except KeyboardInterrupt:
                                click.secho(
                                    "Error calculating the periodogram.", fg='red')
                                flag = 1
                        else:
                            self.rm_background()
                            del self.noise.time
                            del self.noise.bins
                            del self.noise.z2n
                            self.plot_figure()
                            self.data.set_parameters()
                            self.plot_figure()
                            self.data.get_parameters()
                    else:
                        if click.confirm("Do you want to add a background file"):
                            self.plot_background()
                        self.plot_figure()
                        self.data.set_parameters()
                        self.plot_figure()
                        self.data.get_parameters()
                else:
                    flag = 1
            else:
                flag = 1
        else:
            click.secho("The time series file is needed.", fg='yellow')
            if not self.data.set_time():
                if not self.data.set_bins():
                    try:
                        plt.close()
                        self.data.set_periodogram()
                        self.plot_figure()
                        self.data.set_parameters()
                        self.plot_figure()
                        self.data.get_parameters()
                        if click.confirm("Do you want to add a background file"):
                            self.plot_background()
                    except KeyboardInterrupt:
                        click.secho(
                            "Error calculating the periodogram.", fg='red')
                        self.data.z2n = np.array([])
                        flag = 1
                else:
                    flag = 1
            else:
                flag = 1
        return flag

    def crop_region(self) -> int:
        """Change limits on a periodogram region."""
        flag = 0
        click.secho("This will recalculate the periodogram.", fg='yellow')
        self.plot_figure()
        opt = True
        while opt:
            if click.confirm("Is the region selected"):
                self.axis = plt.gca().get_xlim()
                low = np.where(np.isclose(self.data.bins, self.axis[0], 0.1))
                up = np.where(np.isclose(self.data.bins, self.axis[1], 0.1))
                low = np.rint(np.median(low)).astype(int)
                up = np.rint(np.median(up)).astype(int)
                self.fmin = self.axis[0]
                self.fmax = self.axis[1]
                self.set_delta()
                block = (self.fmax - self.fmin) / np.array(self.delta)
                nbytes = np.array(self.delta).dtype.itemsize * block
                click.secho(
                    f"Computation memory {nbytes * 10e-6} MB", fg='yellow')
                if click.confirm("Run the program with these values"):
                    if nbytes < psutil.virtual_memory()[1]:
                        self.bins = np.arange(self.fmin, self.fmax, self.delta)
                        click.secho('Frequency bins set.', fg='green')
                        self.get_bins()
                        self.time = self.data.time
                        plt.close()
                        self.set_periodogram()
                        size = (self.data.bins.size - (up - low)) + \
                            self.bins.size
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
                        self.data.set_bak()
                        # self.data.get_bak()
                        self.data.bak = h5py.File(self.data.bak, 'a')
                        self.data.bak.create_dataset(
                            'FREQUENCY', data=self.data.bins, compression='lzf')
                        self.data.bak.create_dataset(
                            'POTENCY', data=self.data.z2n, compression='lzf')
                        self.data.bins = self.data.bak['FREQUENCY']
                        self.data.z2n = self.data.bak['POTENCY']
                        del self.time
                        del self.bins
                        del self.z2n
                        del tempx
                        del tempy
                        flag = 0
                        opt = False
                    else:
                        click.secho("Not enough memory available.", fg='red')
                        flag = 1
                else:
                    flag = 1
            else:
                flag = 1
        return flag

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
