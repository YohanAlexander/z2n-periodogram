#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

class Figure():

    def __init__(self, title = 'Periodograma Z2n', x_label = "Frequência (Hz)", 
        y_label = 'Amplitude', file = 'z2n'):
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

def plot(frequencies, statistics):
    
    """
    Plots periodogram and saves into a png file.
    """

    fig = Figure()

    plt.plot(frequencies, statistics)
    plt.title(fig.title)
    plt.xlabel(fig.x_label)
    plt.ylabel(fig.y_label)
    plt.savefig('%s.png' %fig.file)
    print("\nFile saved at %s.png.\n" %fig.file)