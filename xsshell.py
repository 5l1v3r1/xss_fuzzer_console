#!/usr/bin/env python

# import modules
import sys
import intro
import fuzzer

col_d = {
    'RED'  :'\033[0;31;40m',
    'BLUE' :'\033[0;36;40m',
    'GREEN':'\033[0;32;40m',
    'YELLW':'\033[33m',
    'ENDC' :'\033[0m',
    'BOLD' :'\033[1m',
    'LINE' :'\033[4m'}

targetStr = ''

# Gather our code in a main() function
def main(arg):
    # Command line prompt
    cmd = color('[','BLUE') + 'XSS' + color(']','BLUE') + color('> ', 'BOLD')
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

    elif args[0] == 'target' :
        usage = "Usage: target url [-s] \n" \
                "Options: \n\t-s \tSave target"
        if len(args) < 2 :
            print color('Not enough args. \n', 'RED') + usage

        else :
            url = args[1]
            resp = fuzzer.set_target(url)
            if resp != 'Success' :
                print color(resp + '\n', 'RED') + usage
            else :
                global targetStr
                targetStr = url
    elif args[0] == 'spider':
        print 'spidey'

def print_help():
    _ = '   '
    print '\n=== ' + color('Commands','YELLW') + ' ==='
    print _ + color('help','YELLW') + '     print this message.'
    print _ + color('exit','YELLW') + '     exit this terminal.'
    print _ + color('status','YELLW') + '   show status of ' \
                                ' current and finished jobs. '
    print _ + color('info','YELLW') + color(' job_name', 'GREEN') \
            + '   show info about a job.'
    print _ + color('target', 'YELLW') + color(' url', 'GREEN') \
            + '   set the target url for xss analysis.'
    print '================\n'


def color(text, colorStr):
    return col_d[colorStr] + text + col_d['ENDC']


if __name__ == '__main__':
    main(sys.argv)
