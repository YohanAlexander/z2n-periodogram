#! /usr/bin/python
# -*- coding: utf-8 -*-

# Wrapping Header
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright (C) 2019, Z2n Software.' 
__credits__ = ['Yohan Alexander']
__license__ = 'MIT LICENSE'
__version__ = '0.1.0'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'

intro = """
        Z2n Software, a package for periodograms from fits datasets.
        Copyright (C) 2019, and MIT License, by Yohan Alexander.
        Type "help", "copyright", "credits" or "license" for more information.
        """

# Generic/Built-in
import time, sys, os, functools

# Other Libraries
import prompt
import numpy as np

time = np.array([])
phase = np.array([])
periodogram = np.array([])
frequencies = np.arange(1e-4, 1.5e-3, 1e-6)