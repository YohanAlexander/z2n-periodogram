#! /usr/bin/python
# -*- coding: utf-8 -*-

# Wrapping Header

__author__ = 'Yohan Alexander'
__version__ = '0.5.0'
__copyright__ = 'Copyright (C) 2019, Z2n Software, by Yohan Alexander.'
__credits__ = ['''The Z2n Software was developed by Yohan Alexander as part of an undergradute research project, funded by the CNPq Institution, and it is supported by the Open Source community.''']
__license__ = 'MIT LICENSE'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'
__url__ = "https://z2n-periodogram.readthedocs.io"
__intro__ = f"""
        Z2n Software ({__version__}), a program for interactive periodograms.
        Copyright (C) 2019, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.

        If you wish to run the software with the default values type "auto".
        """

# Generic/Built-in

import time, sys, os, functools, webbrowser

# Other Libraries

import plot
import prompt
import numpy as np

# Global Variables

path = ""
peak = 0
fmin = 0
fmax = 0
delta = 0
period = 0
frequency = 0
time = np.array([])
phase = np.array([])
periodogram = np.array([])
frequencies = np.array([])