#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import copy

# Other Libraries
import click
import psutil
import termtables
import numpy as np
import matplotlib.pyplot as plt

# Owned Libraries
from z2n import file
from z2n import stats


class Series:
    """
    A class to represent a time series object.

    Attributes
    ----------
    * `gauss : str`
    > A series object that represents the gaussian fit.
    * `input : str`
    > A string that represents the input file path.
    * `output : str`
    > A string that represents the output file name.
    * `format : str`
    > A string that represents the file format.
    * `time : np.array`
    > An arrray that represents the time series.
    * `bins : np.array`
    > An arrray that represents the frequency bins.
    * `z2n : np.array`
    > An arrray that represents the periodogram.
    * `harmonics : int`
    > An integer that represents the number of harmonics.
    * `oversample : int`
    > An integer that represents the oversample factor.
    * `fmin : float`
    > A float that represents the minimum frequency.
    * `fmax : float`
    > A float that represents the maximum frequency.
    * `delta : float`
    > A float that represents the frequency steps.
    * `exposure : float`
    > A float that represents the exposure period.
    * `sampling : float`
    > A float that represents the sampling rate.
    * `potency : float`
    > A float that represents the peak potency.
    * `frequency : float`
    > A float that represents the peak frequency.
    * `period : float`
    > A float that represents the peak period.
    * `errorf : float`
    > A float that represents the frequency uncertainty.
    * `errorp : float`
    > A float that represents the period uncertainty.
    * `pulsed : float`
    > A float that represents the pulsed fraction.

    Methods
    -------
    """

    def __init__(self) -> None:
        self.gauss = ""
        self.input = ""
        self.output = ""
        self.format = ""
        self.time = np.array([])
        self.bins = np.array([])
        self.z2n = np.array([])
        self.fmin = 0
        self.fmax = 0
        self.delta = 0
        self.harmonics = 0
        self.oversample = 0
        self.exposure = 0
        self.sampling = 0
        self.potency = 0
        self.frequency = 0
        self.errorf = 0
        self.period = 0
        self.errorp = 0
        self.pulsed = 0

    def get_gauss(self) -> str:
        """Return the gaussian series object."""
        return self.gauss

    def set_gauss(self) -> None:
        """Copy the gaussian series object."""
        self.gauss = copy.deepcopy(self)

    def get_input(self) -> str:
        """Return the input file path."""
        click.secho(f"Path of the event file: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        """Change the input file path."""
        self.input = click.prompt("Filename", type=click.Path(exists=True))

    def get_output(self) -> str:
        """Return the output file name."""
        click.secho(f"Name of the file: {self.output}", fg='cyan')
        return self.output

    def set_output(self) -> None:
        """Change the output file name."""
        self.output = click.prompt("Name of the file", type=click.Path())

    def get_format(self) -> str:
        """Return the file format."""
        click.secho(f"File format: {self.format}", fg='cyan')
        return self.format

    def set_format(self) -> None:
        """Change the file format."""
        self.format = click.prompt("Format [ascii, csv, fits, hdf5]")

    def get_time(self) -> np.array:
        """Return the time series."""
        click.secho(f"{self.time.size} events.", fg='cyan')
        return self.time

    def set_time(self) -> int:
        """Change the time series."""
        flag = 0
        if not self.load_file():
            self.set_exposure()
            self.set_sampling()
            self.get_time()
            self.get_exposure()
            self.get_sampling()
        else:
            flag = 1
        return flag

    def get_bins(self) -> np.array:
        """Return the frequency steps."""
        click.secho(f"{self.bins.size} frequency steps.", fg='cyan')
        return self.bins

    def set_bins(self) -> int:
        """Change the frequency steps."""
        flag = 1
        click.secho("The frequency range is needed (Hz).", fg='yellow')
        if self.bins.size:
            self.set_delta()
        elif click.confirm(
                "Nyquist frequency as the minimum frequency", prompt_suffix='? '):
            self.fmin = self.sampling * 2
            self.set_fmax()
            self.set_oversample()
            self.delta = 1 / (self.oversample * self.exposure)
        else:
            self.set_fmin()
            self.set_fmax()
            self.set_delta()
        self.get_fmin()
        self.get_fmax()
        self.get_delta()
        block = (self.fmax - self.fmin) / np.array(self.delta)
        nbytes = np.array(self.delta).dtype.itemsize * block
        click.secho(
            f"Computation memory {nbytes * 10e-6} MB", fg='yellow')
        if click.confirm("Run the program with these values", prompt_suffix='? '):
            if nbytes < psutil.virtual_memory()[1]:
                self.bins = np.arange(self.fmin, self.fmax, self.delta)
                self.get_bins()
                self.set_harmonics()
                flag = 0
            else:
                click.secho("Not enough memory available.", fg='red')
                flag = 1
        return flag

    def get_periodogram(self) -> np.array:
        """Return the periodogram."""
        click.secho(f"{self.z2n.size} spectrum steps.", fg='cyan')
        return self.z2n

    def set_periodogram(self) -> None:
        """Change the periodogram."""
        self.time = np.array(self.time)
        self.bins = np.array(self.bins)
        self.z2n = np.zeros(self.bins.size)
        stats.periodogram(self)
        click.secho('Periodogram calculated.', fg='green')
        self.save_file()

    def get_fmin(self) -> float:
        """Return the minimum frequency."""
        click.secho(f"Minimum frequency: {self.fmin} Hz", fg='cyan')
        return self.fmin

    def set_fmin(self) -> None:
        """Change the minimum frequency."""
        self.fmin = click.prompt("Minimum frequency (Hz)", type=float)

    def get_fmax(self) -> float:
        """Return the maximum frequency."""
        click.secho(f"Maximum frequency: {self.fmax} Hz", fg='cyan')
        return self.fmax

    def set_fmax(self) -> None:
        """Change the maximum frequency."""
        self.fmax = click.prompt("Maximum frequency (Hz)", type=float)

    def get_delta(self) -> float:
        """Return the frequency steps."""
        click.secho(f"Frequency steps: {self.delta} Hz", fg='cyan')
        return self.delta

    def set_delta(self) -> None:
        """Change the frequency steps."""
        self.delta = click.prompt("Frequency steps (Hz)", type=float)

    def get_oversample(self) -> int:
        """Return the oversample factor."""
        click.secho(f"Oversample factor: {self.oversample}", fg='cyan')
        return self.oversample

    def set_oversample(self) -> None:
        """Change the oversample factor."""
        self.oversample = click.prompt("Oversample factor", type=int)

    def get_harmonics(self) -> int:
        """Return the number of harmonics."""
        click.secho(f"Number of harmonics: {self.harmonics}", fg='cyan')
        return self.harmonics

    def set_harmonics(self) -> None:
        """Change the number of harmonics."""
        self.harmonics = click.prompt("Number of harmonics", type=int)

    def get_exposure(self) -> float:
        """Return the period of exposure."""
        click.secho(f"Exposure time: {self.exposure} s", fg='cyan')
        return self.exposure

    def set_exposure(self) -> None:
        """Change the period of exposure."""
        stats.exposure(self)

    def get_sampling(self) -> float:
        """Return the sampling rate."""
        click.secho(f"Sampling rate: {self.sampling} Hz", fg='cyan')
        return self.sampling

    def set_sampling(self) -> None:
        """Change the sampling rate."""
        stats.sampling(self)

    def get_potency(self) -> float:
        """Return the peak potency."""
        click.secho(f"Peak potency: {self.potency}", fg='cyan')
        return self.potency

    def set_potency(self) -> None:
        """Change the peak potency."""
        stats.potency(self)

    def get_frequency(self) -> float:
        """Return the peak frequency."""
        click.secho(f"Peak frequency: {self.frequency} Hz", fg='cyan')
        return self.frequency

    def set_frequency(self) -> None:
        """Change the peak frequency."""
        stats.frequency(self)

    def get_period(self) -> float:
        """Return the peak period."""
        click.secho(f"Peak period: {self.period} s", fg='cyan')
        return self.period

    def set_period(self) -> None:
        """Change the peak period."""
        stats.period(self)

    def get_pfraction(self) -> float:
        """Return the pulsed fraction."""
        click.secho(f"Pulsed fraction: {self.pulsed * 100} %", fg='cyan')
        return self.pulsed

    def set_pfraction(self) -> None:
        """Change the pulsed fraction."""
        stats.pfraction(self)

    def get_errorf(self) -> float:
        """Return the uncertainty of the frequency."""
        click.secho(f"Frequency Uncertainty: {self.errorf} +/-", fg='cyan')
        return self.errorf

    def set_errorf(self) -> None:
        """Return the uncertainty of the frequency."""
        stats.error(self)

    def get_errorp(self) -> float:
        """Return the uncertainty of the period."""
        click.secho(f"Period Uncertainty: {self.errorp} +/-", fg='cyan')
        return self.errorp

    def set_errorp(self) -> None:
        """Return the uncertainty of the period."""
        stats.error(self)

    def load_file(self) -> int:
        """Load a input file."""
        flag = 0
        self.set_format()
        if self.format == 'ascii':
            self.set_input()
            file.load_ascii(self)
        elif self.format == 'csv':
            self.set_input()
            file.load_csv(self)
        elif self.format == 'fits':
            self.set_input()
            file.load_fits(self)
        elif self.format == 'hdf5':
            self.set_input()
            file.load_hdf5(self)
        else:
            click.secho(f"{self.format} format not supported.", fg='red')
            flag = 1
        return flag

    def save_file(self) -> None:
        """Save a output file."""
        click.secho("Save the periodogram on a file.", fg='yellow')
        self.set_format()
        if self.format == 'ascii':
            self.set_output()
            file.save_ascii(self)
            click.secho(f"File saved at {self.output}.txt", fg='green')
        elif self.format == 'csv':
            self.set_output()
            file.save_csv(self)
            click.secho(
                f"File saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'fits':
            self.set_output()
            file.save_fits(self)
            click.secho(
                f"File saved at {self.output}.{self.format}", fg='green')
        elif self.format == 'hdf5':
            self.set_output()
            file.save_hdf5(self)
            click.secho(
                f"File saved at {self.output}.{self.format}", fg='green')
        else:
            click.secho(f"{self.format} format not supported.", fg='red')

    def plot(self) -> None:
        """Plot the series and the parameters."""
        self.set_potency()
        self.set_frequency()
        self.set_period()
        self.set_pfraction()
        self.set_gauss()
        plt.close()
        plt.ion()
        plt.plot(self.bins, self.z2n)
        stats.error(self.gauss)
        header = ["", "Z2N POWER", "GAUSSIAN FIT"]
        data = [
            ["Potency", self.potency, self.gauss.potency],
            ["Frequency", f"{self.frequency} Hz",
                f"{self.gauss.frequency} Hz"],
            ["Frequency error", "- Hz", f"+/- {self.gauss.errorf} Hz"],
            ["Period", f"{self.period} s", f"{self.gauss.period} s"],
            ["Period error", "- Hz", f"+/- {self.gauss.errorp} s"],
            ["Pulsed Fraction", f"{self.pulsed * 100} %",
                f"{self.gauss.pulsed * 100} %"],
        ]
        termtables.print(data, header)
