#! /usr/bin/python
# -*- coding: utf-8 -*-

# Wrapping Header
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright (C) 2019, Z2n Software.' 
__credits__ = ['''The Z2n Software was developed by Yohan Alexander 
                and is supported by the Open Source community.''']
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

time = np.array([])
phase = np.array([])
periodogram = np.array([])
frequencies = np.arange(1e-4, 1.5e-3, 1e-6)
figure = Figure()