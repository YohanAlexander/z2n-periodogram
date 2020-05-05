#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click

# Other Libraries
import z2n.prompt as prompt


def cli() -> None:
    """
    Entry point to the Z2n Software.
    """

    try:

        prompt.z2n()

    except Exception as error:
        click.secho(f'{error}', fg='red')


if __name__ == "__main__":
    cli()
