# Command Line Interface

To start the software just type `z2n` on the terminal (check if you're under the virtual environment that it is installed).

The `CLI` of the software is very interactive and it works by triggering the commands available, for more information on the usage type `help`.

```sh
        Z2n Software (1.0.0), a program for interactive periodograms.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.

(z2n) >>> help

Documented commands (type help <topic>):
========================================
axis  back  docs  plot  run  save

Undocumented commands:
======================
exit  help  quit

(z2n) >>>
```

# Colors on the terminal

If available on your terminal emulator, the Z2n software uses colors for providing better insight on the current status of the program execution.

* Sucess

Any time the program sucessfully executes a task, it will indicate with the color <strong style="color:green">green.</strong>

* Warnings

Any time the program is waiting to execute a task, it will indicate with the color <strong style="color:yellow">yellow.</strong>

* Errors

Any time the program encouters errors during a task, it will indicate with the color <strong style="color:red">red.</strong>

* Output

Any time the program outputs a important value, it will indicate with the color <strong style="color:cyan">cyan.</strong>

# Calculating the Z2n potency

The Z2n statistics involves many steps in its calculation, to load a fits file
and just follow the program orientations.

::: z2n.prompt.run
    :docstring:

# Changing the frequency axis

If you are not satisfied with the limits on the frequency axis, or the frequency steps used on the statistics, you can recalculate the periodogram.

::: z2n.prompt.axis
    :docstring:

# Adding background file

If you want to compare the resulting periodogram to a background file, you can easily add one to analyse across shared frequency axis.

::: z2n.prompt.back
    :docstring:

# Saving the periodogram to a file

To save the resulting periodogram (Frequency x Potency) just choose across the current available file formats [ascii, csv, fits].

::: z2n.prompt.save
    :docstring:
