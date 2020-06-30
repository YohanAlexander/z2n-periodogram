# Command Line Interface

Currently there are 2 alternatives provided to interact with the core of the $`Z^2_n`$ Software:

* Passing the desired parameters directly on the terminal as [arguments](#passing-arguments-on-the-terminal).
* Or by a command line interface `CLI`.

To start the interface just type `z2n` on the terminal (check if you're under the virtual environment that it is installed). The `CLI` of the software is very interactive and it works by triggering the commands available, for more information on the usage type `help`.

```bash
z2n

        Z2n Software, a package for interactive periodograms analysis.
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

# Passing arguments on the terminal

To get all available arguments and their correct use, just type `z2n --help` on the terminal (check if you're under the virtual environment that it is installed).

```bash
z2n --help

Usage: z2n [OPTIONS] COMMAND [ARGS]...

  This program allows the user to calculate periodograms, given a time
  series, using the Z2n statistics a la Buccheri et al. 1983.

  The standard Z2n statistics calculates the phase of each arrival time and
  the corresponding sinusoidal functions for each time. Be advised that this
  is very computationally expensive if the number of frequency bins is high.

Options:
  --input PATH                    Name of the input file.
  --output PATH                   Name of the output file.
  --fmin FLOAT                    Minimum frequency on the spectrum (Hz).
  --fmax FLOAT                    Maximum frequency on the spectrum (Hz).
  --delta FLOAT                   Frequency steps on the spectrum (Hz).
  --over INTEGER                  Oversample factor instead of steps.
  --harm INTEGER                  Number of harmonics.  [default: 1]
  --ext INTEGER                   FITS extension number.  [default: 1]
  --format [ascii|csv|fits|hdf5]  Format of the output file.  [default: fits]
  --image [png|pdf|ps|eps]        Format of the image file.  [default: ps]
  --xlabel TEXT                   X label of the image file.  [default:
                                  Frequency (Hz)]

  --ylabel TEXT                   Y label of the image file.  [default: Power]
  --title TEXT                    Title of the image file.
  --docs                          Open the documentation and exit.
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  docs  Open the documentation on the software.
  log   Save the fit of a gaussian curve.
  plot  Open the interactive plotting window.
  run   Calculate the Z2n Statistics.
  save  Save the periodogram on a file.
```

# Colors on the terminal

If available on your terminal emulator, the $`Z^2_n`$ software uses colors for providing better insight on the current status of the program execution.

!!! Important

        * **Sucess**

        Any time the program sucessfully executes a task, it will indicate with the color <strong style="color:green">green.</strong>

!!! Warning

        * **Warnings**

        Any time the program is waiting to execute a task, it will indicate with the color <strong style="color:yellow">yellow.</strong>

!!! Error

        * **Errors**

        Any time the program encouters errors during a task, it will indicate with the color <strong style="color:red">red.</strong>

!!! Note

        * **Output**

        Any time the program outputs a important value, it will indicate with the color <strong style="color:cyan">cyan.</strong>
