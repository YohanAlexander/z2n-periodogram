#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import numpy as np
import matplotlib.pyplot as plt

# Wrapping Header
__version__ = '1.0.3'
__author__ = 'Yohan Alexander'
__license__ = 'MIT LICENSE'
__copyright__ = 'Copyright (C) 2020, Z2n Software, by Yohan Alexander.'
__description__ = 'A program for interative periodograms analysis.'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Developer'
__docs__ = 'https://z2n-periodogram.readthedocs.io'
__url__ = 'https://github.com/yohanalexander/z2n-periodogram'
__credits__ = '''
        The Z2n Software was developed by Yohan Alexander as a research project,
        funded by the CNPq Institution, and it is a Open Source initiative.
        '''
__intro__ = f'''
        Z2n Software ({__version__}), a program for interactive periodograms.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.
        '''
__plot__ = '''
        Interactive plotting window of the Z2n Software.
        Type "help" for more information.
        '''

# Global Variables
axis = 0
fits = 0
band = 0
peak = 0
fmin = 0
fmax = 0
delta = 0
error = 0
forest = 0
period = 0
pulsed = 0
frequency = 0
time = np.array([])
noise = np.array([])
periodogram = np.array([])
frequencies = np.array([])
background = np.array([])
figure, axes = plt.subplots()
