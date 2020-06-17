[![PyPI](https://img.shields.io/pypi/v/z2n-periodogram)](https://pypi.org/project/z2n-periodogram/)
[![GitHub issues](https://img.shields.io/github/issues/yohanalexander/z2n-periodogram)](https://github.com/yohanalexander/z2n-periodogram/issues)
[![GitHub](https://img.shields.io/github/license/yohanalexander/z2n-periodogram)](https://github.com/YohanAlexander/z2n-periodogram/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/z2n-periodogram/badge/?version=latest)](https://z2n-periodogram.readthedocs.io/en/latest/?badge=latest)

<br>
<p align="center">
  <a href="https://github.com/yohanalexander/z2n-periodogram">
    <img src="https://user-images.githubusercontent.com/39287022/84617670-23675480-aea6-11ea-90ac-93a32c01bb92.png" alt="Logo" width="50%" height="50%">
  </a>

  <h1 align="center">Z2n Periodogram</h1>

  <p align="center">
    A program for interative periodograms analysis!
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

The Z2n Software was developed by Yohan Alexander as a research project, funded by the CNPq Institution, and it is a Open Source initiative. The program allows the user to calculate periodograms using the Z2n statistics a la Buccheri et al. 1983, which is defined as follows.

![\Large \phi_j \[0,1\] = frac(v_i\Delta t_{ij} + \dot v_i \frac{\Delta t^2_{ij}}{2} + \dot v_i \frac{\Delta t^3_{ij}}{6})](https://render.githubusercontent.com/render/math?math=%5CLarge%20%5Cphi_j%20%5B0%2C1%5D%20%3D%20frac(v_i%5CDelta%20t_%7Bij%7D%20%2B%20%5Cdot%20v_i%20%5Cfrac%7B%5CDelta%20t%5E2_%7Bij%7D%7D%7B2%7D%20%2B%20%5Cdot%20v_i%20%5Cfrac%7B%5CDelta%20t%5E3_%7Bij%7D%7D%7B6%7D))

![\Large Z^2_n = \frac{2}{N} \cdot \sum_{k=1}^{n} \[(\sum_{j=1}^{N} cos(k\phi_j)) ^ 2 + (\sum_{j=1}^{N} sin(k\phi_j)) ^ 2\]](https://render.githubusercontent.com/render/math?math=%5CLarge%20Z%5E2_n%20%3D%20%5Cfrac%7B2%7D%7BN%7D%20%5Ccdot%20%5Csum_%7Bk%3D1%7D%5E%7Bn%7D%20%5B(%5Csum_%7Bj%3D1%7D%5E%7BN%7D%20cos(k%5Cphi_j))%20%5E%202%20%2B%20(%5Csum_%7Bj%3D1%7D%5E%7BN%7D%20sin(k%5Cphi_j))%20%5E%202%5D)

The standard Z2n statistics calculates the phase of each photon and the sinusoidal functions above for each photon. Be advised that this is very computationally expensive if the number of photons is high, since the algorithm grows at a exponential rate ![\large O(n^2)](https://render.githubusercontent.com/render/math?math=%5Clarge%20O(n%5E2)).


### Built With
The Z2n Software was built using the `Python` open source language.
* [Python](https://python.org)


## Getting Started

### Prerequisites

The version of the `Python` interpreter used during the development was the`3.7`, which can be managed in virtual environments such as `Anaconda`. Therefore, try to use the same or above versions for the best compatibility.

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

The `CLI` of the software is very interactive and it works by triggering the commands available, for more information on the usage type `help`.

```sh
        Z2n Software, a program for interactive periodograms analysis.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.

(z2n) >>> help

Documented commands (type help <topic>):
========================================
docs  log  plot  run  save

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

All content © 2020 Yohan Alexander. Distributed under the MIT License. See <a href="https://github.com/YohanAlexander/z2n-periodogram/blob/master/LICENSE">LICENSE</a> for more information.
