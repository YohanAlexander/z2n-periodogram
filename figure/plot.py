#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def savefig(frequencies, statistics, figure):
    """
    Plots periodogram and saves into a png file.
    """
    
    try:
        plt.plot(frequencies, statistics)
        plt.title(figure.title)
        plt.xlabel(figure.x_label)
        plt.ylabel(figure.y_label)
        plt.savefig('%s.png' %figure.file)
    
    except Exception as error:
        print(error)
