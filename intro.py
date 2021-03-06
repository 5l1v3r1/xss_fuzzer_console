#!/usr/bin/env python

import sys
import os
import random
from time import sleep

"""
Module to print opening sequence
"""

xss = "================================\n" \
      "Y88b   d88P .d8888b.  .d8888b.  \n" \
      " Y88b d88P d88P  Y88bd88P  Y88b \n" \
      "  Y88o88P  Y88b.     Y88b.      \n" \
      "   Y888P    \"Y888b.   \"Y888b.   \n" \
      "   d888b       \"Y88b.    \"Y88b. \n" \
      "  d88888b        \"888      \"888 \n" \
      " d88P Y88b Y88b  d88PY88b  d88P \n" \
      "d88P   Y88b \"Y8888P\"  \"Y8888P\"  \n" \
      "================================\n" \

xs = "=====================\n" \
     "Y88b   d88P .d8888b. \n" \
     " Y88b d88P d88P  Y88b\n" \
     "  Y88o88P  Y88b.     \n" \
     "   Y888P    \"Y888b.  \n" \
     "   d888b       \"Y88b.\n" \
     "  d88888b        \"888\n" \
     " d88P Y88b Y88b  d88P\n" \
     "d88P   Y88b \"Y8888P\" \n" \
     "=====================\n" \

x = "===========\n" \
    "Y88b   d88P\n" \
    " Y88b d88P \n" \
    "  Y88o88P  \n" \
    "   Y888P   \n" \
    "   d888b   \n" \
    "  d88888b  \n" \
    " d88P Y88b \n" \
    "d88P   Y88b\n" \
    "===========\n"


def cls():
    """ function to clear terminal window between output """
    os.system('cls' if os.name == 'nt' else 'clear')


def show(arg):
    """
    Print out X S S by building the string in the terminal window
    Print out welcome line
    """
    RED = '\033[0;31;40m'
    BLUE = '\033[0;36;40m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

    if (len(arg) > 1) and (arg[1] == '-x'):
        return

    cls()
    print RED + x + ENDC
    sleep(0.5)
    cls()
    print RED + xs + ENDC
    sleep(0.5)
    cls()
    print RED + xss + ENDC
    sleep(0.5)

    print (BLUE + 'Welcome to xss terminal, type ' + ENDC
           + BOLD + 'help' + ENDC + BLUE + ' to see commands' + ENDC + '\n')


if __name__ == '__main__':
    """ Basic main function """
    show()
    get_quote()
