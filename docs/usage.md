# Command Line Interface

To start the software just type `z2n` on the terminal (check if you're under the virtual environment that it is installed).

The `CLI` of the software is very interactive, for more information on the usage type `help`.

    	Z2n Software (1.0.0), a package for interactive periodograms.
    	Copyright (C) 2019, and MIT License, by Yohan Alexander [UFS].
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

## Help

::: src.cli.prompt.docs
    :docstring:

::: src.cli.prompt.copyright
    :docstring:

::: src.cli.prompt.version
    :docstring:

::: src.cli.prompt.credits
    :docstring:

::: src.cli.prompt.license
    :docstring:

## Auto Running

To auto run the software with the default values.

::: src.cli.prompt.auto
    :docstring:

## Loading FITS data

This program accepts fits files (.fits) and it is assumed that contains a header with the event or time series data.

::: src.cli.prompt.data
    :docstring:

## Changing the output spectrum

::: src.cli.prompt.rate
    :docstring:

## Calculating the Z2n potency

::: src.cli.prompt.stats
    :docstring:

## Saving the spectrum on file

::: src.cli.prompt.ascii
    :docstring:

## Shell commands inside the cli

::: src.cli.prompt.shell
    :docstring:
