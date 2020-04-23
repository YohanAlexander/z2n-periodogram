#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import time
import sys
import os
import functools

# Other Libraries
from src.cli import globals


def main() -> int:
    """
    Entry point to Z2n Software.
    """

    globals.prompt.cli()

    return 0


if __name__ == "__main__":
    main()
