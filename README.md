
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/yohanalexander/z2n-periodogram/master)
![PyPI](https://img.shields.io/pypi/v/z2n-periodogram)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/z2n-peridogram)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/z2n-periodogram)
![GitHub issues](https://img.shields.io/github/issues/yohanalexander/z2n-periodogram)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yohanalexander/z2n-periodogram)
![GitHub](https://img.shields.io/github/license/yohanalexander/z2n-periodogram)


<p align="center">
  <a href="https://github.com/yohanalexander/z2n-periodogram">
    <img src="assets/z2n.png" alt="Logo" width="50%" height="50%">
  </a>

  <h1 align="center">Z2n Periodogram</h1>

  <p align="center">
    A package for periodograms from FITS datasets!
    <br />
    <a href="https://z2n-periodogram.readthedocs.io/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/yohanalexander/z2n-periodogram">View Demo</a>
    ·
    <a href="https://github.com/yohanalexander/z2n-periodogram/issues">Report Bug</a>
    ·
    <a href="https://github.com/yohanalexander/z2n-periodogram/issues">Request Feature</a>
  </p>


## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)


## About The Project

The Z2n Software is a python package for optimized periodograms from fits datasets. It program allows the user to calculate periodograms using the Z2n statistics a la Buccheri et al. 1983.

<p align="center"><img src="https://rawgit.com/in	git@github.com:YohanAlexander/z2n-periodogram/None/svgs/b978f5d179d91490c920c7e96494ab53.svg?invert_in_darkmode" align=middle width=299.8248pt height=37.583864999999996pt/></p>

<p align="center"><img src="https://rawgit.com/in	git@github.com:YohanAlexander/z2n-periodogram/None/svgs/0205cc14fa865169e21fc457d3de3c48.svg?invert_in_darkmode" align=middle width=342.51194999999996pt height=50.04351pt/></p>

The standard Z2n statistics calculates the phase of each photon and the
sinusoidal functions above for each photon. Be advised that this is very computationally expensive if the number of photons is high.

### Built With
The Z2n Software was built using the open source language `Python`.
* [Python](https://python.org)


## Getting Started

### Prerequisites

The version of the `Python` interpreter used during the development was the`3.7`, which can be managed in virtual environments such as `Anaconda`. Therefore, try to use the same version or one above.

* Python>=3.7
* PIP

### Installation

The software is currently hosted at the Python central repository `PyPI`,  to install the software properly use the terminal command:
```sh
pip install z2n-periodogram
```

## Usage

To start the software just type `z2n` on the terminal (check if you're under the virtual environment that it is installed).
```sh
z2n
```
The `CLI` of the software is very interactive, for more information on the usage type `help`.
```sh
	Z2n Software (1.0.0), a package for interactive periodograms.
	Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
	Type "help" for more information or "docs" for documentation.

	If you wish to run the software with the default values type "auto".

(z2n) >>> help

Documented commands (type help <topic>):
========================================
ascii  copyright  data  license  rate   stats
auto   credits    docs  plot     shell  version

Undocumented commands:
======================
exit  help  quit

(z2n) >>>
```

_For more examples, please refer to the [Documentation](https://z2n-periodogram.readthedocs.io/)_


## Roadmap

See the [open issues](https://github.com/yohanalexander/z2n-periodogram/issues) for a list of proposed features (and known issues).


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

All content © 2020 Yohan Alexander. Distributed under the MIT License. See `LICENSE` for more information.

  <a href="https://opensource.org/licenses">
    <img src="assets/opensource.png" alt="OpenSource" width="25%" height="25%">
  </a>
  <a href="https://github.com/YohanAlexander/z2n-periodogram/blob/master/LICENSE">
    <img src="assets/license.png" alt="MIT" width="25%" height="25%">
  </a>

