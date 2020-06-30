# Prerequisites

The version of the `Python` interpreter used during the development was the `3.7`, which can be managed in virtual environments such as [Anaconda](https://docs.conda.io/en/latest/index.html). Therefore, try to use the same or above versions for the best compatibility.

* Python>=3.7
* PIP

## Installation

The software is currently hosted at the `Python` central repository [PyPI](https://pypi.org/project/z2n-periodogram/),  to install the software properly use the command on the terminal:

```bash
pip install -U z2n-periodogram
```

## Known Issues

!!! Warning

    To create an interactive plotting window (where the user is able to select regions on   the power spectrum) this package requires the bult-in python module [Tkinter](https://docs.python.org/3/library/tkinter.html). Although the module should arrive with any **Python** installation, it may be missing. In that case, a manual installation of the  module will be required.

    The module is available on the package managers of the major **linux** distributions.

    For **debian** based distros:

    ```
    $ sudo apt install python3-tk
    ```

    For **fedora** based distros:

    ```
    $ sudo dnf install python3-tkinter
    ```

    For **arch** based distros:

    ```
    $ sudo pacman -S tk
    ```

    For other systems consult the avaible [docs on the module](https://tkdocs.com/tutorial/ install.html).
