#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import numpy as np

def save_ascii(periodogram: np.array, frequencies: np.array, text: str) -> None:
    """
    Saves the frequency spectrum into an formatted ascii file.

    Parameters
    ----------
    frequencies : numpy.array
        Numpy array that represents the frequency spectrum.
    periodogram : numpy.array
        Numpy array that represents the power spectrum of each frequency on the spectrum.
    text : str
        A formatted String that represents the name of the output file.

    Returns
    -------
    None
    """

    try:
        
        with open(f'{text}', 'w') as file:

            for spec, freq in zip(periodogram, frequencies):
                file.write(str(freq) + " " + str(spec) + "\n")
        
        click.echo(f"Text file saved at {text}")
        

    except Exception as error:
        click.echo(error)
