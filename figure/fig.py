#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib import rc

rc('font', family='serif')
rc('text', usetex=True)
rc('xtick', labelsize=8)
rc('ytick', labelsize=8)
rc('axes', labelsize=8)

#style.use('science')

def savefig(frequencies, statistics, name):
    """
    Plots periodogram and saves into a png file.
    """
    
    try:
        plt.ion()
        plt.tight_layout()
        plt.plot(frequencies, statistics, label="Z2n Statistics")
        plt.legend()
        plt.savefig("%s.png" %name)
        plt.show()
    
    except Exception as error:
        print(error)