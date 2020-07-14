#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import pathlib

# Other Libraries
import click
import numpy as np
from astropy.io import fits
from astropy.table import Table


def load_file(series, ext) -> int:
    """
    Open file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    flag = 0
    suffix = pathlib.Path(series.input).suffix
    if suffix in ("", ".txt"):
        flag = load_ascii(series)
    elif suffix in (".csv", ".ecsv"):
        flag = load_csv(series)
    elif suffix in (".hdf", ".h5", ".hdf5", ".he5"):
        flag = load_hdf5(series)
    else:
        with fits.open(series.input) as events:
            try:
                events['Z2N']
                click.secho('Z2N extension already found', fg='yellow')
                if click.confirm('Use the periodogram', prompt_suffix='? '):
                    series.bins = events['Z2N'].data['FREQUENCY']
                    series.bins = series.bins.astype(series.bins.dtype.name)
                    series.z2n = events['Z2N'].data['POWER']
                    series.z2n = series.z2n.astype(series.z2n.dtype.name)
                    hdr = events['Z2N'].header
                    series.exposure = float(hdr['exposure'])
                    series.sampling = float(hdr['sampling'])
                    series.nyquist = float(hdr['nyquist'])
                    series.harmonics = int(hdr['harmonic'])
                    series.fmin = float(hdr['fmin'])
                    series.fmax = float(hdr['fmax'])
                    series.delta = float(hdr['delta'])
                    series.frequency = float(hdr['peak'])
                    series.period = float(hdr['period'])
                    series.power = float(hdr['power'])
                    series.pulsed = float(hdr['pulsed'])
                    click.secho(f"{hdr['events']} events.", fg='cyan')
                    series.get_exposure()
                    series.get_sampling()
                    series.get_nyquist()
                    series.get_fmin()
                    series.get_fmax()
                    series.get_delta()
                    series.get_bins()
                    series.get_harmonics()
                    series.get_frequency()
                    series.get_period()
                    series.get_power()
                    series.get_pfraction()
                    series.set_gauss()
                    series.set_bak()
                    load_fits(series, ext)
                    flag = 1
                else:
                    flag = load_fits(series, ext)
            except KeyError:
                flag = load_fits(series, ext)
    return flag


def load_ascii(series) -> int:
    """
    Open ascii file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    flag = 1
    table = Table.read(series.input, format='ascii')
    try:
        series.time = table['TIME'].data
        series.time = series.time.astype(series.time.dtype.name)
        flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                table.pprint()
                click.secho(f"Column {column} not found.", fg='red')
                column = click.prompt(
                    "Which column name", type=str, prompt_suffix='? ')
                series.time = table[column].data
                series.time = series.time.astype(series.time.dtype.name)
                if click.confirm(f"Use column {column}", prompt_suffix='? '):
                    flag = 0
                else:
                    click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


def load_csv(series) -> int:
    """
    Open csv file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    flag = 1
    table = Table.read(series.input, format='csv')
    try:
        series.time = table['TIME'].data
        series.time = series.time.astype(series.time.dtype.name)
        flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                table.pprint()
                click.secho(f"Column {column} not found.", fg='red')
                column = click.prompt(
                    "Which column name", type=str, prompt_suffix='? ')
                series.time = table[column].data
                series.time = series.time.astype(series.time.dtype.name)
                if click.confirm(f"Use column {column}", prompt_suffix='? '):
                    flag = 0
                else:
                    click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


def load_fits(series, ext) -> None:
    """
    Open fits file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    flag = 0
    times = 0
    columns = ['TIME', 'time']
    extensions = []
    with fits.open(series.input) as events:
        if ext:
            try:
                series.time = events[ext].data['TIME']
                series.time = series.time.astype(series.time.dtype.name)
                click.secho(
                    f"Column TIME in {events[ext].name}.", fg='yellow')
                flag = 0
            except (KeyError, TypeError):
                flag = 1
                click.secho(
                    f"Column TIME not found in {events[ext].name}.", fg='red')
            except IndexError:
                flag = 1
                click.secho(
                    f"Extension number {ext} not found.", fg='red')
        else:
            for hdu in range(1, len(events)):
                try:
                    if any(column in events[hdu].columns.names for column in columns):
                        extensions.append(hdu)
                        times += 1
                except AttributeError:
                    pass
            if times == 1:
                click.secho(
                    f"Column TIME in {events[extensions[0]].name}.", fg='yellow')
                series.time = events[extensions[0]].data['TIME']
                series.time = series.time.astype(series.time.dtype.name)
                flag = 0
            elif times > 1:
                click.secho("Multiple columns TIME found.", fg='yellow')
                flag = 1
                while flag:
                    table = Table(
                        names=('Number', 'Extension', 'Length (Rows)'),
                        dtype=('int64', 'str', 'int64'))
                    for value in extensions:
                        table.add_row([
                            value,
                            events[value].name,
                            events[value].data['TIME'].size])
                    table.pprint()
                    number = click.prompt(
                        "Which extension number", type=int, prompt_suffix='? ')
                    try:
                        if click.confirm(f"Use column in {events[number].name}"):
                            series.time = events[number].data['TIME']
                            series.time = series.time.astype(
                                series.time.dtype.name)
                            flag = 0
                            break
                        else:
                            flag = 1
                            click.clear()
                    except (KeyError, TypeError):
                        flag = 1
                        click.clear()
                        click.secho(
                            f"Column TIME not found in {events[number].name}.",
                            fg='red')
                    except IndexError:
                        flag = 1
                        click.clear()
                        click.secho(
                            f"Extension number {number} not found.", fg='red')
            else:
                click.clear()
                column = 'TIME'
                flag = 1
                while flag:
                    hdu = 1
                    while hdu < len(events):
                        table = Table(events[hdu].data)
                        table.pprint()
                        click.secho(
                            f"Column {column} not found in extension.", fg='red')
                        click.secho(
                            f"Extension {events[hdu].name}.", fg='yellow')
                        if click.confirm("Use extension [y] or go to next [n]"):
                            try:
                                column = click.prompt(
                                    "Which column name", type=str, prompt_suffix='? ')
                                series.time = events[hdu].data[column]
                                series.time = series.time.astype(
                                    series.time.dtype.name)
                                if click.confirm(
                                        f"Use column {column}", prompt_suffix='? '):
                                    flag = 0
                                    break
                                else:
                                    flag = 1
                                    click.clear()
                            except (KeyError, TypeError):
                                flag = 1
                                click.clear()
                            except IndexError:
                                flag = 1
                                click.clear()
                                click.secho(
                                    f"Extension number {hdu} not found.", fg='red')
                        else:
                            flag = 1
                            hdu += 1
                            click.clear()
    return flag


def load_hdf5(series) -> int:
    """
    Open hdf5 file and store time series.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    flag = 1
    table = Table.read(series.input, format='hdf5')
    try:
        series.time = table['TIME'].data
        series.time = series.time.astype(series.time.dtype.name)
        flag = 0
    except (KeyError, TypeError, IndexError):
        click.clear()
        column = 'TIME'
        flag = 1
        while flag:
            try:
                table.pprint()
                click.secho(f"Column {column} not found.", fg='red')
                column = click.prompt(
                    "Which column name", type=str, prompt_suffix='? ')
                series.time = table[column].data
                series.time = series.time.astype(series.time.dtype.name)
                if click.confirm(f"Use column {column}", prompt_suffix='? '):
                    flag = 0
                else:
                    click.clear()
            except (KeyError, TypeError, IndexError):
                click.clear()
    return flag


def save_ascii(series) -> None:
    """
    Save the periodogram to ascii file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('FREQUENCY', 'POWER'))
    table.write(f'{series.output}.txt', format='ascii')


def save_csv(series) -> None:
    """
    Save the periodogram to csv file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('FREQUENCY', 'POWER'))
    table.write(f'{series.output}.csv', format='csv')


def save_fits(series) -> None:
    """
    Save the periodogram to fits file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    suffix = pathlib.Path(series.input).suffix
    if suffix in ("", ".txt", ".csv", ".ecsv", ".hdf", ".h5", ".hdf5", ".he5"):
        primary_hdu = fits.PrimaryHDU()
        bins = fits.Column(
            name='FREQUENCY', array=series.bins, format='D', unit='Hz')
        z2n = fits.Column(name='POWER', array=series.z2n, format='D')
        hdr = fits.Header()
        hdr['EXTNAME'] = 'Z2N'
        hdr.comments['EXTNAME'] = 'Name of this extension'
        hdr['HDUNAME'] = 'Z2N'
        hdr.comments['HDUNAME'] = 'Name of the hdu'
        hdr['events'] = f'{series.time.size}'
        hdr.comments['events'] = 'Number of events'
        hdr['exposure'] = f'{series.exposure}'
        hdr.comments['exposure'] = 'Exposure time (Texp)'
        hdr['sampling'] = f'{series.sampling}'
        hdr.comments['sampling'] = 'Sampling rate (1/Texp)'
        hdr['nyquist'] = f'{series.nyquist}'
        hdr.comments['nyquist'] = 'Nyquist 2*(1/Texp)'
        hdr['harmonic'] = f'{series.harmonics}'
        hdr.comments['harmonic'] = 'Number of harmonics'
        hdr['steps'] = f'{series.z2n.size}'
        hdr.comments['steps'] = 'Number of steps'
        hdr['fmin'] = f'{series.fmin}'
        hdr.comments['fmin'] = 'Minimum frequency'
        hdr['fmax'] = f'{series.fmax}'
        hdr.comments['fmax'] = 'Maximum frequency'
        hdr['delta'] = f'{series.delta}'
        hdr.comments['delta'] = 'Frequency steps'
        hdr['peak'] = f'{series.frequency}'
        hdr.comments['peak'] = 'Global peak frequency'
        hdr['period'] = f'{series.period}'
        hdr.comments['period'] = 'Global peak period'
        hdr['power'] = f'{series.power}'
        hdr.comments['power'] = 'Global peak power'
        hdr['pulsed'] = f'{series.pulsed}'
        hdr.comments['pulsed'] = 'Global pulsed fraction'
        try:
            hdr['gpeak'] = f'{series.gauss.frequency}'
            hdr.comments['gpeak'] = 'Gauss peak frequency'
            hdr['gperiod'] = f'{series.gauss.period}'
            hdr.comments['gperiod'] = 'Gauss peak period'
            hdr['gpower'] = f'{series.gauss.power}'
            hdr.comments['gpower'] = 'Gauss peak power'
            hdr['gpulsed'] = f'{series.gauss.pulsed}'
            hdr.comments['gpulsed'] = 'Gauss pulsed fraction'
        except AttributeError:
            pass
        table_hdu = fits.BinTableHDU.from_columns([bins, z2n], header=hdr)
        hdul = fits.HDUList([primary_hdu, table_hdu])
        hdul.writeto(f'{series.output}.fits')
    else:
        with fits.open(series.input) as events:
            bins = fits.Column(
                name='FREQUENCY', array=series.bins, format='D', unit='Hz')
            z2n = fits.Column(name='POWER', array=series.z2n, format='D')
            hdr = fits.Header()
            hdr['EXTNAME'] = 'Z2N'
            hdr.comments['EXTNAME'] = 'Name of this extension'
            hdr['HDUNAME'] = 'Z2N'
            hdr.comments['HDUNAME'] = 'Name of the hdu'
            hdr['events'] = f'{series.time.size}'
            hdr.comments['events'] = 'Number of events'
            hdr['exposure'] = f'{series.exposure}'
            hdr.comments['exposure'] = 'Exposure time (Texp)'
            hdr['sampling'] = f'{series.sampling}'
            hdr.comments['sampling'] = 'Sampling rate (1/Texp)'
            hdr['nyquist'] = f'{series.nyquist}'
            hdr.comments['nyquist'] = 'Nyquist 2*(1/Texp)'
            hdr['harmonic'] = f'{series.harmonics}'
            hdr.comments['harmonic'] = 'Number of harmonics'
            hdr['steps'] = f'{series.z2n.size}'
            hdr.comments['steps'] = 'Number of steps'
            hdr['fmin'] = f'{series.fmin}'
            hdr.comments['fmin'] = 'Minimum frequency'
            hdr['fmax'] = f'{series.fmax}'
            hdr.comments['fmax'] = 'Maximum frequency'
            hdr['delta'] = f'{series.delta}'
            hdr.comments['delta'] = 'Frequency steps'
            hdr['peak'] = f'{series.frequency}'
            hdr.comments['peak'] = 'Global peak frequency'
            hdr['period'] = f'{series.period}'
            hdr.comments['period'] = 'Global peak period'
            hdr['power'] = f'{series.power}'
            hdr.comments['power'] = 'Global peak power'
            hdr['pulsed'] = f'{series.pulsed}'
            hdr.comments['pulsed'] = 'Global pulsed fraction'
            try:
                hdr['gpeak'] = f'{series.gauss.frequency}'
                hdr.comments['gpeak'] = 'Gauss peak frequency'
                hdr['gperiod'] = f'{series.gauss.period}'
                hdr.comments['gperiod'] = 'Gauss peak period'
                hdr['gpower'] = f'{series.gauss.power}'
                hdr.comments['gpower'] = 'Gauss peak power'
                hdr['gpulsed'] = f'{series.gauss.pulsed}'
                hdr.comments['gpulsed'] = 'Gauss pulsed fraction'
            except AttributeError:
                pass
            hdu = fits.BinTableHDU.from_columns([bins, z2n], header=hdr)
            events.append(hdu)
            events.writeto(f'{series.output}.fits')


def save_hdf5(series) -> None:
    """
    Save the periodogram to hdf5 file.

    Parameters
    ----------
    series : Series
        A time series object.

    Returns
    -------
    None
    """
    array = np.column_stack((series.bins, series.z2n))
    table = Table(array, names=('FREQUENCY', 'POWER'))
    table.write(f'{series.output}.hdf5', path='z2n',
                format='hdf5', compression=True)
