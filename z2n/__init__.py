#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
from pkg_resources import get_distribution
from pkg_resources import DistributionNotFound

__project__ = 'z2n-periodogram'
__version__ = None
__license__ = 'MIT'
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright (C) 2020, Z2n Software, by Yohan Alexander.'
__description__ = 'A program for interative periodograms analysis.'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Development'
__credits__ = 'Yohan Alexander'
__docs__ = 'https://z2n-periodogram.readthedocs.io'
__url__ = 'https://github.com/yohanalexander/z2n-periodogram'

try:
    __version__ = get_distribution(__project__).version
except DistributionNotFound:
    VERSION = __project__ + '-' + '(local)'
else:
    VERSION = __project__ + '-' + __version__
    import click
    import matplotlib
    try:
        matplotlib.use('tkagg')
    except ImportError:
        click.secho("Failed to use interactive backend.", fg='red')
        click.secho(
            "Check Tkinter dependency: sudo apt-get install python3-tk""", fg='yellow')
