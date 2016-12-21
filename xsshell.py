#!/usr/bin/env python

# import modules
import sys
import intro

class color:
    RED   = '\033[0;31;40m'
    BLUE  = '\033[0;36;40m'
    GREEN = '\033[0;32;40m'
    ENDC  = '\033[0m'
    BOLD  = '\033[1m'
    LINE  = '\033[4m'

# Gather our code in a main() function
def main():
    intro.show()
    while 1 :
        input = raw_input(color.RED + "[XSS]> " + color.ENDC)



if __name__ == '__main__':
    main()
