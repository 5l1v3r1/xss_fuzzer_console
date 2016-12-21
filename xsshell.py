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

# 

# Command line prompt
cmd = color.BLUE + "[" + color.ENDC + "XSS" + color.BLUE + "]" + color.ENDC \
    + color.BOLD + "> " + color.ENDC

# Gather our code in a main() function
def main(arg):
  intro.show(arg)
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
  _ = '   '
  print '\n=== ' + color.YELLW + 'Commands' + color.ENDC + ' ==='
  print _ + color.YELLW + 'help' + color.ENDC + '     print this message.'
  print _ + color.YELLW + 'exit' + color.ENDC + '     exit this terminal.'
  print _ + color.YELLW + 'status' + color.ENDC + '   show status of ' \
                              ' current and finished jobs. '
  print _ + color.YELLW + 'info' + color.ENDC + color.GREEN + ' job_name' \
              + color.ENDC + '   show info about a job.'
  print _ + color.YELLW + 'target' + color.ENDC + color.GREEN + ' url' \
              + color.ENDC + '   set the target url for xss analysis.'
  print '================\n'

if __name__ == '__main__':
    main(sys.argv)
