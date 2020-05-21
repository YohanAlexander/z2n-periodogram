#! /usr/bin/python
# -*- coding: utf-8 -*-

# Owned Libraries
from z2n import prompt


def cli() -> int:
    """Entry point to the Z2n Software."""
    try:
        prompt.z2n()
    except SystemExit:
        return 0


if __name__ == "__main__":
    cli()
