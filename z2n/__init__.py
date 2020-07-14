#! /usr/bin/python
# -*- coding: utf-8 -*-

__project__ = 'z2n-periodogram'
__version__ = '2.0.4'
__license__ = 'MIT'
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright (C) 2020, Z2n Software, by Yohan Alexander.'
__description__ = 'A package for interative periodograms analysis.'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Development'
__credits__ = 'Yohan Alexander'
__docs__ = 'https://z2n-periodogram.readthedocs.io'
__url__ = 'https://github.com/yohanalexander/z2n-periodogram'

import click
import matplotlib
try:
    matplotlib.use('tkagg')
except (ImportError, ModuleNotFoundError):
    click.secho("Failed to use interactive backend.", fg='red')
    click.secho(
        "Check Tkinter dependency: sudo apt-get install python3-tk""", fg='yellow')
