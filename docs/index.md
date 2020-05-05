# Welcome to the Z2n Periodogram Documentation

[![PyPI](https://img.shields.io/pypi/v/z2n-periodogram)](https://pypi.org/project/z2n-periodogram/)
[![GitHub issues](https://img.shields.io/github/issues/yohanalexander/z2n-periodogram)](https://github.com/yohanalexander/z2n-periodogram/issues)
[![GitHub](https://img.shields.io/github/license/yohanalexander/z2n-periodogram)](https://github.com/YohanAlexander/z2n-periodogram/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/z2n-periodogram/badge/?version=latest)](https://z2n-periodogram.readthedocs.io/en/latest/?badge=latest)

<br>
<p align="center">
  <a href="https://github.com/yohanalexander/z2n-periodogram">
    <img src="https://user-images.githubusercontent.com/39287022/80550543-cb789b00-8996-11ea-90af-fe2936fb703e.png" alt="Logo" width="50%" height="50%">
  </a>

  <h1 align="center">Z2n Periodogram</h1>

  <p align="center">
    A program for interative periodograms analysis!

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](/install/#getting-started)
* [Usage](/usage)
* [Plotting](/plotting)
* [Contributing](/contribute)
* [Roadmap](/contribute#roadmap)
* [License](/copyright)

## About The Project

The Z2n Software was developed by Yohan Alexander as a research project, funded by the CNPq Institution, and it is a Open Source initiative. The program allows the user to calculate periodograms, from fits datasets, using the Z2n statistics a la Buccheri et al. 1983, which is defined as follows.

<p align="center"><img src="svgs/b978f5d179d91490c920c7e96494ab53.svg?invert_in_darkmode" align=middle width=299.8248pt height=37.583864999999996pt/></p>

<p align="center"><img src="svgs/0205cc14fa865169e21fc457d3de3c48.svg?invert_in_darkmode" align=middle width=342.51194999999996pt height=50.04351pt/></p>

The standard Z2n statistics calculates the phase of each photon and the sinusoidal functions above for each photon. Be advised that this is very computationally expensive if the number of photons is high, since the algorithm grows at a exponential rate <img src="svgs/3987120c67ed5a9162aa9841b531c3a9.svg?invert_in_darkmode" align=middle width=43.022265pt height=26.76201000000001pt/>.

## Built With

The Z2n Software was built using the `Python` open source language.

* [Python](https://python.org)
