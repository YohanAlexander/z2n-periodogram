#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import tempfile

# Other Libraries
import h5py
import click
import psutil
import numpy as np

# Owned Libraries
from z2n import file
from z2n import stats


class Series:
    """
    A class to represent a time series object.

    Attributes
    ----------
    * `bak : str`
    > A string that represents the backup file path.
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
    > A float that represents the frequency uncertainty.
    * `noise : float`
    > A float that represents the period uncertainty.
    * `pulsed : float`
    > A float that represents the pulsed fraction.
    * `forest : float`
    > A float that represents the potency uncertainty.
    * `bandwidth : float`
    > A float that represents the bandwidth potency.

    Methods
    -------
    """

    def __init__(self) -> None:
        self.bak = ""
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
        self.observation = 0
        self.sampling = 0
        self.potency = 0
        self.forest = 0
        self.bandwidth = 0
        self.frequency = 0
        self.error = 0
        self.period = 0
        self.noise = 0
        self.pulsed = 0

    def get_bak(self) -> str:
        """Return the backup file path."""
        click.secho(f"Path of the backup: {self.bak}", fg='cyan')
        return self.bak

    def set_bak(self) -> None:
        """Change the backup file path."""
        self.bak = tempfile.NamedTemporaryFile(
            suffix='.z2n', delete=False).name

    def get_input(self) -> str:
        """Return the input file path."""
        click.secho(f"Path of the time series: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        """Change the input file path."""
        self.input = click.prompt(
            "Path of the time series", type=click.Path(exists=True))

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
        self.format = click.prompt("Which format [ascii, csv, fits, hdf5]")

    def get_time(self) -> np.array:
        """Return the time series."""
        click.secho(f"{self.time.size} time values.", fg='cyan')
        return self.time

    def set_time(self) -> int:
        """Change the time series."""
        flag = 0
        if not self.load_file():
            self.time = self.time.astype(self.time.dtype.name)
            self.set_observation()
            self.set_sampling()
            self.get_time()
            self.get_observation()
            self.get_sampling()
        else:
            flag = 1
        return flag

    def get_bins(self) -> np.array:
        """Return the frequency bins."""
        click.secho(f"{self.bins.size} frequency bins.", fg='cyan')
        return self.bins

    def set_bins(self) -> int:
        """Change the frequency bins."""
        flag = 1
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
        block = (self.fmax - self.fmin) / np.array(self.delta)
        nbytes = np.array(self.delta).dtype.itemsize * block
        click.secho(
            f"Computation memory {nbytes * 10e-6} MB", fg='yellow')
        if click.confirm("Run the program with these values"):
            if nbytes < psutil.virtual_memory()[1]:
                self.bins = np.arange(self.fmin, self.fmax, self.delta)
                click.secho('Frequency bins set.', fg='green')
                self.get_bins()
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
        self.set_harmonics()
        self.z2n = np.zeros(self.bins.size)
        stats.periodogram(self)
        click.secho('Periodogram calculated.', fg='green')
        # self.set_parameters()
        self.set_bak()
        # self.get_bak()
        self.bak = h5py.File(self.bak, 'a')
        self.bak.create_dataset('FREQUENCY', data=self.bins, compression='lzf')
        self.bak.create_dataset('POTENCY', data=self.z2n, compression='lzf')
        del self.bins
        del self.z2n
        self.bins = self.bak['FREQUENCY']
        self.z2n = self.bak['POTENCY']

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

    def get_oversample(self) -> int:
        """Return the oversample factor."""
        click.secho(f"Oversample factor: {self.oversample}", fg='cyan')
        return self.oversample

    def set_oversample(self) -> None:
        """Change the oversample factor."""
        self.oversample = click.prompt("Oversample factor", type=int)
        click.secho('Oversample factor set.', fg='green')

    def get_harmonics(self) -> int:
        """Return the number of harmonics."""
        click.secho(f"Number of harmonics: {self.harmonics}", fg='cyan')
        return self.harmonics

    def set_harmonics(self) -> None:
        """Change the number of harmonics."""
        self.harmonics = click.prompt("Number of harmonics", type=int)
        click.secho('Harmonics set.', fg='green')

    def get_observation(self) -> float:
        """Return the period of observation."""
        click.secho(f"Exposure time: {self.observation} s", fg='cyan')
        return self.observation

    def set_observation(self) -> None:
        """Change the period of observation."""
        stats.observation(self)
        click.secho('Exposure time set.', fg='green')

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
        click.secho(
            f"Peak potency: {self.potency} +/- {self.forest}", fg='cyan')
        return self.potency

    def set_potency(self) -> None:
        """Change the peak potency."""
        stats.potency(self)
        click.secho('Peak potency set.', fg='green')

    def get_frequency(self) -> float:
        """Return the peak frequency."""
        click.secho(
            f"Peak frequency: {self.frequency} +/- {self.error} Hz", fg='cyan')
        return self.frequency

    def set_frequency(self) -> None:
        """Change the peak frequency."""
        stats.frequency(self)
        click.secho('Peak frequency set.', fg='green')

    def get_period(self) -> float:
        """Return the peak period."""
        click.secho(
            f"Peak period: {self.period} +/- {self.noise} s", fg='cyan')
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
        stats.gauss(self)
        click.secho('Frequency uncertainty set.', fg='green')

    def get_noise(self) -> float:
        """Return the uncertainty of the period."""
        click.secho(f"Period Uncertainty: {self.noise} +/-", fg='cyan')
        return self.noise

    def set_noise(self) -> None:
        """Return the uncertainty of the period."""
        stats.gauss(self)
        click.secho('Period uncertainty set.', fg='green')

    def load_file(self) -> int:
        """Load a input file."""
        flag = 0
        self.set_format()
        if self.format == 'ascii':
            self.set_input()
            file.load_ascii(self)
            click.secho("File loaded.", fg='green')
        elif self.format == 'csv':
            self.set_input()
            file.load_csv(self)
            click.secho("File loaded.", fg='green')
        elif self.format == 'fits':
            self.set_input()
            file.load_fits(self)
            click.secho("File loaded.", fg='green')
        elif self.format == 'hdf5':
            self.set_input()
            file.load_hdf5(self)
            click.secho("File loaded.", fg='green')
        else:
            click.secho(f"{self.format} format not supported.", fg='red')
            flag = 1
        return flag

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
        elif self.format == 'hdf5':
            self.set_output()
            file.save_hdf5(self)
            click.secho(f"Saved at {self.output}.{self.format}", fg='green')
        else:
            click.secho(f"{self.format} format not supported.", fg='red')

    def get_parameters(self) -> None:
        """Return the parameters used on the statistic."""
        self.get_bandwidth()
        self.get_potency()
        # self.get_forest()
        self.get_frequency()
        # self.get_error()
        self.get_period()
        # self.get_noise()
        self.get_pfraction()

    def set_parameters(self) -> None:
        """Change the parameters used on the statistic."""
        self.set_potency()
        self.set_forest()
        self.set_bandwidth()
        self.set_frequency()
        self.set_error()
        self.set_period()
        self.set_noise()
        self.set_pfraction()
