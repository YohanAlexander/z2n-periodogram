# Welcome to the Z2n Periodogram Documentation

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/yohanalexander/z2n-periodogram/master)
![PyPI](https://img.shields.io/pypi/v/z2n-periodogram)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/z2n-peridogram)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/z2n-periodogram)
![GitHub issues](https://img.shields.io/github/issues/yohanalexander/z2n-periodogram)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yohanalexander/z2n-periodogram)
![GitHub](https://img.shields.io/github/license/yohanalexander/z2n-periodogram)

<br />
<p align="center">
  <a href="https://github.com/yohanalexander/z2n-periodogram">
    <img src="../assets/z2n.png" alt="Logo" width="50%" height="50%">
  </a>

  <h1 align="center">Z2n Periodogram</h1>

  <p align="center">
    A package for periodograms from FITS datasets!

## Table of Contents

* [About the Project](#about-the-project)
    * [Built With](#built-with)
* [Getting Started](/install/#getting-started)
    * [Prerequisites](/install/#prerequisites)
    * [Installation](/install/#installation)
* [Usage](/usage)
    *  [Loading FITS file](/usage/#loading-fits-data)
    *  [Run with default values](/usage/#auto-running)
    *  [Change the output spectrum](/usage/#changing-the-output-spectrum)
    *  [Calculating the Z2n Potency](/usage/#calculating-the-z2n-potency)
    *  [Saving an ascii file](/usage/#saving-the-spectrum-on-file)
    *  [Shell commands](/usage/#shell-commands-inside-the-cli)
    *  [Import as a library](/usage/#importing-the-software-as-a-library)
* [Plotting](/plotting)
    * [Change Plot Axes](/plotting/#changing-the-plot-axes)
    * [Plot with a grid](/plotting/#plot-with-a-grid)
    * [Change the Plot Title](/plotting/#change-the-plot-title)
    * [Change the x label](/plotting/#change-the-x-label)
    * [Change the y label](/plotting/#change-the-y-label)
    * [Save image file](/plotting/#save-plot-figure)
* [Contributing](/contribute)
* [Roadmap](/contribute#roadmap)
* [License](/copyright)

## About The Project

The Z2n Software is a python package for optimized periodograms from fits datasets. The program allows the user to calculate periodograms using the Z2n statistics a la Buccheri et al. 1983, which is defined as follows.

<p align="center"><img src="https://rawgit.com/in	git@github.com:YohanAlexander/z2n-periodogram/master/svgs/b978f5d179d91490c920c7e96494ab53.svg?invert_in_darkmode" align=middle width=299.8248pt height=37.583864999999996pt/></p>

<p align="center"><img src="https://rawgit.com/in	git@github.com:YohanAlexander/z2n-periodogram/master/svgs/0205cc14fa865169e21fc457d3de3c48.svg?invert_in_darkmode" align=middle width=342.51194999999996pt height=50.04351pt/></p>

The standard Z2n statistics calculates the phase of each photon and the
sinusoidal functions above for each photon. Be advised that this is very computationally expensive, if the number of photons is high. Since the algorithm grows at a exponential rate. <p align="center"><img src="https://rawgit.com/in	git@github.com:YohanAlexander/z2n-periodogram/master/svgs/28de126d9302a6049e582fda13ec4441.svg?invert_in_darkmode" align=middle width=43.022265pt height=18.312359999999998pt/></p>

## Built With

The Z2n Software was built using the open source language `Python`.

* [Python](https://python.org)
