#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import csv
import copy
import psutil
import pathlib
import tempfile

# Other Libraries
import h5py
import click
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
    * `bak : str`
    > A string that represents the backup file path.
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
    * `nyquist : float`
    > A float that represents the nyquist frequency.
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
        self.bak = ""
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
        self.nyquist = 0
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

    def get_bak(self) -> str:
        """Return the backup file path."""
        click.secho(f"Path of the backup: {self.bak}", fg='cyan')
        return self.bak

    def set_bak(self) -> None:
        """Change the backup file path."""
        self.bak = tempfile.NamedTemporaryFile(
            suffix='.z2n', delete=False).name
        self.bak = h5py.File(self.bak, 'a')
        self.bak.create_dataset('TIME', data=self.time, compression='lzf')
        self.bak.create_dataset('BINS', data=self.bins, compression='lzf')
        self.bak.create_dataset('Z2N', data=self.z2n, compression='lzf')
        del self.time
        del self.bins
        del self.z2n
        self.time = self.bak['TIME']
        self.bins = self.bak['BINS']
        self.z2n = self.bak['Z2N']

    def get_input(self) -> str:
        """Return the input file path."""
        click.secho(f"Path of the event file: {self.input}", fg='cyan')
        return self.input

    def set_input(self) -> None:
        """Change the input file path."""
        self.input = click.prompt(
            "Filename", self.input, type=click.Path(exists=True))

    def get_output(self) -> str:
        """Return the output file name."""
        click.secho(f"Name of the file: {self.output}", fg='cyan')
        return self.output

    def set_output(self) -> None:
        """Change the output file name."""
        default = "z2n_" + pathlib.Path(self.input).stem
        flag = 1
        while flag:
            self.output = click.prompt(
                "Name of the file", default, type=click.Path())
            if pathlib.Path(f"{self.output}.{self.format}").is_file():
                click.secho("File already exists.", fg='red')
            else:
                flag = 0

    def get_format(self) -> str:
        """Return the file format."""
        click.secho(f"File format: {self.format}", fg='cyan')
        return self.format

    def set_format(self) -> None:
        """Change the file format."""
        self.format = click.prompt(
            "Format", "fits", type=click.Choice(['ascii', 'csv', 'fits', 'hdf5']))

    def get_time(self) -> np.array:
        """Return the time series."""
        click.secho(f"{self.time.size} events.", fg='cyan')
        return self.time

    def set_time(self) -> int:
        """Change the time series."""
        flag = 0
        self.set_input()
        if not file.load_file(self, 0):
            click.secho('Event file loaded.', fg='green')
            self.set_exposure()
            self.set_sampling()
            self.set_nyquist()
            self.get_time()
            self.get_exposure()
            self.get_sampling()
            self.get_nyquist()
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
        while flag:
            click.secho("The frequency range is needed (Hz).", fg='yellow')
            if self.bins.size:
                self.set_delta()
            elif click.confirm(
                    "Nyquist as the minimum frequency", prompt_suffix='? '):
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
            self.set_harmonics()
            block = (self.fmax - self.fmin) / np.array(self.delta)
            nbytes = np.array(self.delta).dtype.itemsize * block
            click.secho(
                f"Computation memory {nbytes* 10e-6:.5f} MB", fg='yellow')
            if click.confirm("Run with these values", True, prompt_suffix='? '):
                if nbytes < psutil.virtual_memory()[1]:
                    self.bins = np.arange(self.fmin, self.fmax, self.delta)
                    self.get_bins()
                    flag = 0
                else:
                    click.secho("Not enough memory available.", fg='red')
        return flag

    def get_periodogram(self) -> np.array:
        """Return the periodogram."""
        click.secho(f"{self.z2n.size} spectrum steps.", fg='cyan')
        return self.z2n

    def set_periodogram(self) -> None:
        """Change the periodogram."""
        self.bak = ""
        self.time = np.array(self.time)
        self.bins = np.array(self.bins)
        self.z2n = np.zeros(self.bins.size)
        stats.periodogram(self)
        click.secho('Periodogram calculated.', fg='green')
        self.set_gauss()
        self.set_bak()
        # self.get_bak()
        self.save_file()

    def get_nyquist(self) -> float:
        """Return the nyquist frequency."""
        click.secho(
            f"Nyquist 2*(1/Texp): {self.nyquist:.1e} Hz", fg='cyan')
        return self.nyquist

    def set_nyquist(self) -> None:
        """Change the nyquist frequency."""
        stats.exposure(self)
        stats.sampling(self)
        self.nyquist = 2 * self.sampling

    def get_fmin(self) -> float:
        """Return the minimum frequency."""
        click.secho(f"Minimum frequency: {self.fmin:.1e} Hz", fg='cyan')
        return self.fmin

    def set_fmin(self) -> None:
        """Change the minimum frequency."""
        self.fmin = click.prompt("Minimum frequency (Hz)", type=float)

    def get_fmax(self) -> float:
        """Return the maximum frequency."""
        click.secho(f"Maximum frequency: {self.fmax:.1e} Hz", fg='cyan')
        return self.fmax

    def set_fmax(self) -> None:
        """Change the maximum frequency."""
        self.fmax = click.prompt("Maximum frequency (Hz)", type=float)

    def get_delta(self) -> float:
        """Return the frequency steps."""
        click.secho(f"Frequency steps: {self.delta:.1e} Hz", fg='cyan')
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
        self.harmonics = click.prompt("Number of harmonics", 1, type=int)

    def get_exposure(self) -> float:
        """Return the period of exposure."""
        click.secho(f"Exposure time (Texp): {self.exposure:.1f} s", fg='cyan')
        return self.exposure

    def set_exposure(self) -> None:
        """Change the period of exposure."""
        stats.exposure(self)

    def get_sampling(self) -> float:
        """Return the sampling rate."""
        click.secho(
            f"Sampling rate (1/Texp): {self.sampling:.1e} Hz", fg='cyan')
        return self.sampling

    def set_sampling(self) -> None:
        """Change the sampling rate."""
        stats.sampling(self)

    def get_potency(self) -> float:
        """Return the peak potency."""
        click.secho(f"Peak power: {self.potency:.5f}", fg='cyan')
        return self.potency

    def set_potency(self) -> None:
        """Change the peak potency."""
        stats.potency(self)

    def get_frequency(self) -> float:
        """Return the peak frequency."""
        click.secho(f"Peak frequency: {self.frequency:.5f} Hz", fg='cyan')
        return self.frequency

    def set_frequency(self) -> None:
        """Change the peak frequency."""
        stats.frequency(self)

    def get_period(self) -> float:
        """Return the peak period."""
        click.secho(f"Peak period: {self.period:.5f} s", fg='cyan')
        return self.period

    def set_period(self) -> None:
        """Change the peak period."""
        stats.period(self)

    def get_pfraction(self) -> float:
        """Return the pulsed fraction."""
        click.secho(f"Pulsed fraction: {self.pulsed * 100:.5f} %", fg='cyan')
        return self.pulsed

    def set_pfraction(self) -> None:
        """Change the pulsed fraction."""
        stats.pfraction(self)

    def get_errorf(self) -> float:
        """Return the uncertainty of the frequency."""
        click.secho(f"Frequency Uncertainty: {self.errorf:.5f} +/-", fg='cyan')
        return self.errorf

    def set_errorf(self) -> None:
        """Return the uncertainty of the frequency."""
        stats.error(self)

    def get_errorp(self) -> float:
        """Return the uncertainty of the period."""
        click.secho(f"Period Uncertainty: {self.errorp:.5f} +/-", fg='cyan')
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
            file.load_fits(self, 0)
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
        flag = 1
        while flag:
            self.set_potency()
            self.set_frequency()
            self.set_period()
            self.set_pfraction()
            self.gauss.time = np.array(self.time)
            self.gauss.bins = np.array(self.bins)
            self.gauss.z2n = np.array(self.z2n)
            plt.close()
            plt.ion()
            plt.plot(self.bins, self.z2n, label='Z2n Power', linewidth=2)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power')
            plt.legend(loc='best')
            plt.tight_layout()
            try:
                stats.error(self.gauss)
                header = ["", "Z2N POWER", "GAUSSIAN FIT"]
                data = [
                    ["Power", f"{self.potency:.5f}",
                        f"{self.gauss.potency:.5f}"],
                    ["Frequency", f"{self.frequency:.5f} Hz",
                        f"{self.gauss.frequency:.5f} Hz"],
                    ["Frequency error", "_",
                        f"+/- {self.gauss.errorf:.5f} Hz"],
                    ["Period", f"{self.period:.5f} s",
                        f"{self.gauss.period:.5f} s"],
                    ["Period error", "_", f"+/- {self.gauss.errorp:.5f} s"],
                    ["Pulsed Fraction", f"{self.pulsed* 100:.5f} %",
                        f"{self.gauss.pulsed* 100:.5f} %"],
                ]
                termtables.print(data, header)
                plt.close()
                plt.ion()
                plt.plot(self.bins, self.z2n, label='Z2n Power', linewidth=2)
                plt.plot(
                    self.gauss.bins, self.gauss.z2n,
                    color='tab:red', label='Gaussian Fit', linewidth=1)
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Power')
                plt.legend(loc='best')
                plt.tight_layout()
            except IndexError:
                click.secho("Error on the selection.", fg='red')
            else:
                if not click.confirm("Select another region for the fit"):
                    flag = 0
                    click.secho("Save the results on a log file.", fg='yellow')
                    default = "z2n_" + pathlib.Path(self.input).stem
                    flag2 = 1
                    while flag2:
                        log = click.prompt(
                            "Name of the file", default, type=click.Path())
                        if pathlib.Path(f"{log}.log").is_file():
                            click.secho("File already exists.", fg='red')
                        else:
                            flag2 = 0
                            with open(f"{log}.log", "w+") as logfile:
                                writer = csv.writer(
                                    logfile, delimiter=',', quoting=csv.QUOTE_NONE)
                                writer.writerow(header)
                                writer.writerows(data)
                            click.secho(
                                f"Saved the results at {log}.log", fg='green')
