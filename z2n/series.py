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

    Attributes
    ----------
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
    * `observation : float`
    > A float that represents the observation period.
    * `sampling : float`
    > A float that represents the sampling rate.
    * `potency : float`
    > A float that represents the peak potency.
    * `frequency : float`
    > A float that represents the peak frequency.
    * `period : float`
    > A float that represents the peak period.
    * `error : float`
    > A float that represents the uncertainty.
    * `pulsed : float`
    > A float that represents the pulsed fraction.
    * `forest : float`
    > A float that represents the forest potency.
    * `bandwidth : float`
    > A float that represents the bandwidth potency.

    Methods
    -------
    """

    def __init__(self) -> None:
        self.input = ""
        self.output = ""
        self.format = ""
        self.time = np.array([])
        self.bins = np.array([])
        self.z2n = np.array([])
        self.harmonics = 1
        self.fmin = 0
        self.fmax = 0
        self.delta = 0
        self.oversample = 0
        self.observation = 0
        self.sampling = 0
        self.potency = 0
        self.forest = 0
        self.bandwidth = 0
        self.frequency = 0
        self.error = 0
        self.period = 0
        self.pulsed = 0

    def get_input(self) -> str:
        """Return the input file path."""
        click.secho(f"Path of the file: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        """Change the input file path."""
        self.input = click.prompt(
            "Path of the file", type=click.Path(exists=True))

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
        self.format = click.prompt("Which format [ascii, csv, fits]")

    def get_time(self) -> np.array:
        """Return the time series."""
        click.secho(f"{self.time.size} time values.", fg='cyan')
        return self.time

    def set_time(self) -> None:
        """Change the time series."""
        self.load_file()

    def get_bins(self) -> np.array:
        """Return the frequency bins."""
        click.secho(f"{self.bins.size} frequency bins.", fg='cyan')
        return self.bins

    def set_bins(self) -> None:
        """Change the frequency bins."""
        self.set_sampling()
        if click.confirm("Do you want to use the Nyquist frequency"):
            self.fmin = self.sampling * 2
            self.set_fmax()
            self.set_oversample()
            self.delta = 1 / (self.oversample * self.observation)
            self.get_fmin()
            self.get_fmax()
            self.get_delta()
        else:
            self.set_fmin()
            self.set_fmax()
            self.set_delta()
            self.get_fmin()
            self.get_fmax()
            self.get_delta()
        self.bins = np.arange(self.fmin, self.fmax, self.delta)
        click.secho('Frequency bins set.', fg='green')

    def get_periodogram(self) -> np.array:
        """Return the periodogram."""
        click.secho(f"{self.z2n.size} potency values.", fg='cyan')
        return self.z2n

    def set_periodogram(self) -> None:
        """Change the periodogram."""
        self.time = self.time.astype('float64')
        self.z2n = np.zeros(self.bins.size)
        stats.periodogram(self)
        click.secho('Periodogram calculated.', fg='green')

    def get_fmin(self) -> float:
        """Return the minimum frequency."""
        click.secho(f"Minimum frequency: {self.fmin} Hz", fg='cyan')
        return self.fmin

    def set_fmin(self) -> None:
        """Change the minimum frequency."""
        self.fmin = click.prompt("Minimum frequency", type=float)
        click.secho('Minimum frequency set.', fg='green')

    def get_fmax(self) -> float:
        """Return the maximum frequency."""
        click.secho(f"Maximum frequency: {self.fmax} Hz", fg='cyan')
        return self.fmax

    def set_fmax(self) -> None:
        """Change the maximum frequency."""
        self.fmax = click.prompt("Maximum frequency", type=float)
        click.secho('Maximum frequency set.', fg='green')

    def get_delta(self) -> float:
        """Return the frequency steps."""
        click.secho(f"Frequency steps: {self.delta} Hz", fg='cyan')
        return self.delta

    def set_delta(self) -> None:
        """Change the frequency steps."""
        self.delta = click.prompt("Frequency steps", type=float)
        click.secho('Frequency steps set.', fg='green')

    def get_oversample(self) -> float:
        """Return the oversample factor."""
        click.secho(f"Oversample factor: {self.oversample}", fg='cyan')
        return self.oversample

    def set_oversample(self) -> None:
        """Change the oversample factor."""
        self.oversample = click.prompt("Oversample factor", type=float)
        click.secho('Oversample factor set.', fg='green')

    def get_harmonics(self) -> float:
        """Return the number of harmonics."""
        click.secho(f"Number of harmonics: {self.harmonics}", fg='cyan')
        return self.harmonics

    def set_harmonics(self) -> None:
        """Change the number of harmonics."""
        self.harmonics = click.prompt("Number of harmonics", type=float)
        click.secho('Harmonics set.', fg='green')

    def get_observation(self) -> float:
        """Return the period of observation."""
        click.secho(f"Period of observation: {self.observation} s", fg='cyan')
        return self.observation

    def set_observation(self) -> None:
        """Change the period of observation."""
        stats.observation(self)
        click.secho('Period of observation set.', fg='green')

    def get_sampling(self) -> float:
        """Return the sampling rate."""
        click.secho(f"Sampling frequency: {self.sampling} Hz", fg='cyan')
        return self.sampling

    def set_sampling(self) -> None:
        """Change the sampling rate."""
        stats.sampling(self)
        click.secho('Sampling frequency set.', fg='green')

    def get_potency(self) -> float:
        """Return the peak potency."""
        click.secho(f"Peak potency: {self.potency}", fg='cyan')
        return self.potency

    def set_potency(self) -> None:
        """Change the peak potency."""
        stats.potency(self)
        click.secho('Peak potency set.', fg='green')

    def get_frequency(self) -> float:
        """Return the peak frequency."""
        click.secho(f"Peak frequency: {self.frequency} Hz", fg='cyan')
        return self.frequency

    def set_frequency(self) -> None:
        """Change the peak frequency."""
        stats.frequency(self)
        click.secho('Peak frequency set.', fg='green')

    def get_period(self) -> float:
        """Return the peak period."""
        click.secho(f"Peak period: {self.period} s", fg='cyan')
        return self.period

    def set_period(self) -> None:
        """Change the peak period."""
        stats.period(self)
        click.secho('Peak period set.', fg='green')

    def get_pfraction(self) -> float:
        """Return the pulsed fraction."""
        click.secho(f"Pulsed fraction: {self.pulsed * 100} %", fg='cyan')
        return self.pulsed

    def set_pfraction(self) -> None:
        """Change the pulsed fraction."""
        stats.pfraction(self)
        click.secho('Pulsed fraction set.', fg='green')

    def get_forest(self) -> float:
        """Return the potency uncertainty."""
        click.secho(f"Potency uncertainty: {self.forest}", fg='cyan')
        return self.forest

    def set_forest(self) -> None:
        """Change the forest potency."""
        stats.forest(self)
        click.secho('Potency uncertainty set.', fg='green')

    def get_bandwidth(self) -> float:
        """Return the bandwidth potency."""
        click.secho(f"Bandwidth: {self.bandwidth}", fg='cyan')
        return self.bandwidth

    def set_bandwidth(self) -> None:
        """Change the bandwidth potency."""
        stats.bandwidth(self)
        click.secho('Bandwidth set.', fg='green')

    def get_error(self) -> float:
        """Return the uncertainty of the frequency."""
        click.secho(f"Frequency Uncertainty: {self.error} +/-", fg='cyan')
        return self.error

    def set_error(self) -> None:
        """Return the uncertainty of the frequency."""
        stats.error(self)
        click.secho('Frequency uncertainty set.', fg='green')

    def load_file(self) -> int:
        """Load a input file."""
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
        """Save a output file."""
        self.set_format()
        if self.format == 'ascii':
            self.set_output()
            file.save_ascii(self)
            click.secho(f"Saved at {self.output}.txt", fg='green')
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

    def load_periodogram(self) -> int:
        """Plot the periodogram from a file."""
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

    def save_periodogram(self) -> int:
        """Calculate the Z2n statistic."""
        self.set_bins()
        if click.confirm("Run the program with these values"):
            if not self.set_periodogram():
                self.set_parameters()
                return 0
            else:
                return 1
        else:
            return 1

    def get_parameters(self) -> None:
        """Return the parameters used on the statistic."""
        self.get_time()
        self.get_observation()
        self.get_sampling()
        self.get_fmin()
        self.get_fmax()
        self.get_delta()
        self.get_bins()
        self.get_periodogram()
        self.get_potency()
        self.get_forest()
        self.get_bandwidth()
        self.get_frequency()
        self.get_error()
        self.get_period()
        self.get_pfraction()

    def set_parameters(self) -> None:
        """Change the parameters used on the statistic."""
        self.set_observation()
        self.set_sampling()
        self.set_frequency()
        self.set_period()
        self.set_error()
        self.set_pfraction()
        self.set_potency()
        self.set_forest()
        self.set_bandwidth()
