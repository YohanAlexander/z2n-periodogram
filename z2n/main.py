#! /usr/bin/python
# -*- coding: utf-8 -*-

# Owned Libraries
from z2n import prompt

# Other Libraries
import matplotlib

# Defalt backend
matplotlib.use('qt5agg')


def cli() -> None:
    """Entry point to the Z2n Software."""
    prompt.z2n()


if __name__ == "__main__":
    cli()
