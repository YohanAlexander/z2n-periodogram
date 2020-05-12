#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
import numpy as np

# Owned Libraries
from z2n import file
from z2n import stats


class Series:
    """
    A class to represent a time series object.
    ...
    Attributes
    ----------
    ...
    Methods
    -------
    ...
    """

    def __init__(self) -> None:
        self.input = ""
        self.output = ""
        self.format = ""
        self.time = np.array([])
        self.bins = np.array([])
        self.z2n = np.array([])
        self.pot = 0
        self.fmin = 0
        self.fmax = 0
        self.freq = 0
        self.peak = 0
        self.band = 0
        self.error = 0
        self.delta = 0
        self.period = 0
        self.pulsed = 0
        self.forest = 0

    def get_parameters(self) -> None:
        self.get_time()
        self.get_period()
        self.get_sampling()
        self.get_fmin()
        self.get_fmax()
        self.get_delta()
        self.get_bins()
        self.get_periodogram()
        self.get_frequency()
        self.get_error()
        self.get_pfraction()
        self.get_potency()
        self.get_forest()
        self.get_band()

    def set_parameters(self) -> None:
        self.set_period()
        self.set_sampling()
        self.set_frequency()
        self.set_error()
        self.set_pfraction()
        self.set_potency()
        self.set_forest()
        self.set_band()

    def get_input(self) -> str:
        click.secho(f"Path to the file: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        self.input = click.prompt(
            "Path to the file", type=click.Path(exists=True))

    def get_output(self) -> str:
        click.secho(f"Name of the file: {self.output}", fg='cyan')
        return self.output

    def set_output(self) -> None:
        self.output = click.prompt("Name of the file", type=click.Path())

    def get_format(self) -> str:
        click.secho(f"File format: {self.format}", fg='cyan')
        return self.format

    def set_format(self) -> None:
        self.format = click.prompt("Which format [ascii, csv, fits]")

    def get_time(self) -> np.array:
        click.secho(f"{self.time.size} time values.", fg='cyan')
        return self.time

    def set_time(self) -> None:
        self.load_file()

    def get_fmin(self) -> float:
        click.secho(f"Minimum frequency: {self.fmin} Hz", fg='cyan')
        return self.fmin

    def set_fmin(self) -> None:
        self.fmin = click.prompt("Minimum frequency", type=float)
        click.secho('Minimum frequency set.', fg='green')

    def get_fmax(self) -> float:
        click.secho(f"Maximum frequency: {self.fmax} Hz", fg='cyan')
        return self.fmax

    def set_fmax(self) -> None:
        self.fmax = click.prompt("Maximum frequency", type=float)
        click.secho('Maximum frequency set.', fg='green')

    def get_delta(self) -> float:
        click.secho(f"Frequency steps: {self.delta} Hz", fg='cyan')
        return self.delta

    def set_delta(self) -> None:
        self.delta = click.prompt("Frequency steps", type=float)
        click.secho('Frequency steps set.', fg='green')

    def get_bins(self) -> np.array:
        click.secho(f"{self.bins.size} frequency bins.", fg='cyan')
        return self.bins

    def set_bins(self) -> None:
        self.set_sampling()
        if click.confirm("Do you want to use the Nyquist frequency"):
            self.fmin = self.freq * 2
            self.fmax = self.freq * 100
            self.set_delta()
        else:
            self.set_fmin()
            self.set_fmax()
            self.set_delta()
        self.bins = np.arange(self.fmin, self.fmax, self.delta)
        click.secho('Frequency bins set.', fg='green')

    def get_period(self) -> float:
        click.secho(f"Period of observation: {self.period} s", fg='cyan')
        return self.period

    def set_period(self) -> None:
        stats.period(self)
        click.secho('Period of observation set.', fg='green')

    def get_sampling(self) -> float:
        click.secho(f"Sampling frequency: {self.freq} Hz", fg='cyan')
        return self.freq

    def set_sampling(self) -> None:
        stats.sampling(self)
        click.secho('Sampling frequency set.', fg='green')

    def get_potency(self) -> float:
        click.secho(f"Peak potency: {self.pot}", fg='cyan')
        return self.pot

    def set_potency(self) -> None:
        stats.potency(self)
        click.secho('Peak potency set.', fg='green')

    def get_frequency(self) -> float:
        click.secho(f"Peak frequency: {self.peak} Hz", fg='cyan')
        return self.peak

    def set_frequency(self) -> None:
        stats.frequency(self)
        click.secho('Peak frequency set.', fg='green')

    def get_band(self) -> float:
        click.secho(f"Bandwidth: {self.band}", fg='cyan')
        return self.band

    def set_band(self) -> None:
        stats.bandwidth(self)
        click.secho('Bandwidth set.', fg='green')

    def get_error(self) -> float:
        click.secho(f"Uncertainty: {self.error} +/-", fg='cyan')
        return self.error

    def set_error(self) -> None:
        stats.error(self)
        click.secho('Uncertainty set.', fg='green')

    def get_pfraction(self) -> float:
        click.secho(f"Pulsed fraction: {self.pulsed * 100} %", fg='cyan')
        return self.pulsed

    def set_pfraction(self) -> None:
        stats.pfraction(self)
        click.secho('Pulsed fraction set.', fg='green')

    def get_forest(self) -> float:
        click.secho(f"Forest potency: {self.forest}", fg='cyan')
        return self.forest

    def set_forest(self) -> None:
        stats.forest(self)
        click.secho('Forest potency set.', fg='green')

    def get_periodogram(self) -> np.array:
        click.secho(f"{self.z2n.size} potency values.", fg='cyan')
        return self.z2n

    def set_periodogram(self) -> None:
        self.time = self.time.astype('float64')
        self.z2n = np.zeros(self.bins.size)
        stats.periodogram(self)
        click.secho('Periodogram calculated.', fg='green')

    def load_file(self) -> int:
        self.set_format()
        if self.format == 'ascii':
            self.set_input()
            file.load_ascii(self)
            click.secho("File loaded.", fg='green')
            return 0
        elif self.format == 'csv':
            self.set_input()
            file.load_csv(self)
            click.secho("File loaded.", fg='green')
            return 0
        elif self.format == 'fits':
            self.set_input()
            file.load_fits(self)
            click.secho("File loaded.", fg='green')
            return 0
        else:
            click.secho(f"{self.format} format not supported.", fg='red')
            return 1

    def save_file(self) -> None:
        self.set_format()
        if self.format == 'ascii':
            file.save_ascii(self)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'csv':
            self.set_output()
            file.save_csv(self)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'fits':
            self.set_output()
            file.save_fits(self)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        else:
            click.secho(f"{self.format} format not supported.", fg='red')

    def get_z2n(self) -> int:
        self.set_format()
        if self.format == 'ascii':
            self.set_input()
            file.plot_ascii(self)
            click.secho("File loaded.", fg='green')
            return 0
        elif self.format == 'csv':
            self.set_input()
            file.plot_csv(self)
            click.secho("File loaded.", fg='green')
            return 0
        elif self.format == 'fits':
            self.set_input()
            file.plot_fits(self)
            click.secho("File loaded.", fg='green')
            return 0
        else:
            click.secho(f"{self.format} format not supported.", fg='red')
            return 1

    def set_z2n(self) -> int:
        self.set_bins()
        if not self.set_periodogram():
            self.set_parameters()
            self.get_parameters()
            return 0
        else:
            return 1
