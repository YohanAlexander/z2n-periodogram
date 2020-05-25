#! /usr/bin/python
# -*- coding: utf-8 -*-

# Owned Libraries
from z2n import prompt


def cli() -> None:
    """Entry point to the Z2n Software."""
    try:
        prompt.z2n()
    except SystemExit:
        pass


if __name__ == "__main__":
    cli()
