#! /usr/bin/python
# -*- coding: utf-8 -*-

from astropy.io import fits

def load_fits(path):
    """
    Open fits file and return time series as a numpy array.
    """

    try:
        data = fits.open('%s' %path) # open fits file
        event = data['EVENTS'].data # acesses event header
        time_series = event['TIME'] # stores time series on numpy array
        data.close()
        
        return time_series

    except FileNotFoundError as error:
        print("\n")
        print(error)
        print("\n")