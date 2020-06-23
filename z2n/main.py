#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import matplotlib

# Owned Libraries
from z2n import prompt

# Defalt backend
matplotlib.use('qt5agg')


def cli() -> None:
    """Entry point to the Z2n Software."""
    prompt.z2n()


if __name__ == "__main__":
    cli()
