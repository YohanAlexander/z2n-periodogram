#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import click
import matplotlib


def cli() -> None:
    """Entry point to the Z2n Software."""
    try:
        matplotlib.use('tkagg')
    except (ImportError, ModuleNotFoundError):
        click.secho("Failed to use interactive backend.", fg='red')
        click.secho(
            "Check Tkinter dependency: sudo apt-get install python3-tk""", fg='yellow')
    else:
        # Owned Libraries
        from z2n import prompt
        prompt.z2n()


if __name__ == "__main__":
    cli()
