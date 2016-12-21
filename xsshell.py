#!/usr/bin/env python

# import modules
import sys
import intro

class color:
    RED   = '\033[0;31;40m'
    BLUE  = '\033[0;36;40m'
    GREEN = '\033[0;32;40m'
    YELLW = '\033[33m'
    ENDC  = '\033[0m'
    BOLD  = '\033[1m'
    LINE  = '\033[4m'

# Command line prompt
cmd = color.BLUE + "[XSS]" + color.ENDC + color.BOLD + "> " + color.ENDC

# Gather our code in a main() function
def main():
  intro.show()
  while 1 :
    try:
      input = raw_input(cmd)
      eval(input)
    except EOFError:
      print 'Exiting (Ctrl+D)'
      break

def eval(input):
  args = input.split()
  
  if args[0] in ['h','-h','help','-help']:
    print_help()
  
  elif args[0] in ['exit','-exit']:
    print 'See ya!'
    sys.exit(0)

def print_help():
  print '\n=== ' + color.YELLW + 'Commands' + color.ENDC + ' ==='
  print '   ' + color.YELLW + 'help' + color.ENDC + '   print this message'
  print '   ' + color.YELLW + 'exit' + color.ENDC + '   exit this terminal'
  print '================\n'

if __name__ == '__main__':
    main()
