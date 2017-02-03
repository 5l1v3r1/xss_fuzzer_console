#!/usr/bin/env python

# import modules
import sys
import os
import random
from time import sleep

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
    os.system('cls' if os.name == 'nt' else 'clear')


def show(arg):
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

    if (len(arg) > 1) and (arg[1] == '-q'):
        print get_quote()

    print (BLUE + 'Welcome to my terminal, type ' + ENDC
           + BOLD + 'help' + ENDC + BLUE + ' to see commands' + ENDC + '\n')


def get_quote():

    quotes = ["\"Jerry, just remember... It's not a lie if you believe it\""
              "\n   -- George Costanza",

              "\"You know, if you take everything I've accomplished in my"
              " entire life and condense it down into one day, it looks"
              " decent.\"\n   -- George Costanza",

              "\"You're giving me the 'It's not you, it's me routine?' I"
              " invented 'It's not you, it's me.' Nobody tells me it's them"
              ", not me. If it's anybody, it's me\"\n   -- George Costanza",

              "\"You have the chicken, the hen, and the rooster. The chicken"
              " goes with the hen... So who is having sex with the rooster?\""
              "\n   -- Frank Costanza",

              "\"I don't think I've ever been to an appointment in my life"
              " where I wanted the other guy to show up.\"\n   -- George Costanza",

              "\"Don't insult me, my friend. Remember who you're talking to."
              " No one's a bigger idiot than me.\"\n   -- George Costanza",

              "\"I'm not superstitious, but I am a little stitious.\"\n -- "
              "Michael Scott"


              ]

    return quotes[random.randint(0, len(quotes) - 1)] + '\n'


if __name__ == '__main__':
    show()
    get_quote()
