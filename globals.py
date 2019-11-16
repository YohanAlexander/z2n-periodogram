#! /usr/bin/python
# -*- coding: utf-8 -*-

# Wrapping Header
__author__ = 'Yohan Alexander'
__version__ = '0.2.0'
__copyright__ = 'Copyright (C) 2019, Z2n Software, by Yohan Alexander.'
__credits__ = ['''The Z2n Software was developed by Yohan Alexander and it is supported by the Open Source community.''']
__license__ = 'MIT LICENSE'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'

intro = """
        Z2n Software (%s), a python package for periodograms from fits datasets.
        Type "help", "copyright", "credits", "license" or "docs" for more information.

        If you wish to run the software with the default values type auto.
        """ %__version__

# Generic/Built-in
import time, sys, os, functools, webbrowser

# Other Libraries
import prompt
import numpy as np

class Figure():

    def __init__(self, title="", x_label="", y_label="", file=""):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.file = file

    def set_title(self, t):
        self.title = t

    def set_xlabel(self, x):
        self.x_label = x

    def set_yabel(self, y):
        self.y_label = y
    
    def set_file(self, f):
        self.file = f

fmax = 0
fmin = 0
delta = 0
sample_rate = 0
time = np.array([])
phase = np.array([])
periodogram = np.array([])
frequencies = np.array([])
figure = Figure()