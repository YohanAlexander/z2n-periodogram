#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click

# Other Libraries
from src import prompt


def main() -> int:
    """
    Entry point to the Z2n Software.
    """

    try:

        prompt.cli()

    except Exception as error:
        click.secho(f'{error}', fg='red')

    return 0


if __name__ == "__main__":
    main()
