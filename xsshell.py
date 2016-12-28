#!/usr/bin/env python

# import modules
import sys
import intro
import connect
import threading
import fuzz_thread

col_d = {
    'RED'  :'\033[0;31;40m',
    'BLUE' :'\033[0;36;40m',
    'GREEN':'\033[0;32;40m',
    'YELLW':'\033[33m',
    'ENDC' :'\033[0m',
    'BOLD' :'\033[1m',
    'LINE' :'\033[4m'
    }

config = {
        '-target': '', # Target URL, which defines the initial scope
        '-threads': 1, # Number of threads for spider and attacker
        '-delay': 0,   # Delay in network requests
        '-depth': 3    # Recursive depth when using spider
        }

class usage:
    set = '' 
    def __init__(self):
        self.set = 'usage: ' + color('set', 'YELLW') + color('  [-target URL]'
            + '  [-threads n]  [-delay n]  [-depth n]', 'GREEN') + '\n'\
           'Options: \n' \
           '  -target URL: attack target URL; defines initial scope\n'\
           '  -threads n:  number of threads of execution for attack\n'\
           '  -delay n:    delay, in milliseconds, between network requests\n'\
           '  -depth n:    recursive depth when running spider\n'


queue = None # global object containing spidered links and other metadata 

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
    # Declaring setup variables
    global config
    use = usage()
    args = input.split() # Split arguments into a list
  
    if args[0] in ['h','-h','help','-help']:
        print_help()
  
    elif args[0] in ['exit','-exit']:
        print 'See ya!'
        sys.exit(0)
    elif args[0] == 'set':
        if len(args) < 2:
            print use.set
            return
        for op in args[1:]:
            val_i = args.index(op) + 1
            if (config.get(op) == None) or (val_i >= len(args)):
                continue

            # If setting target, check that URL is valid
            if op == '-target':
                url = args[val_i]
                res = connect.set_target(url)[1]
                if res == 'Success' :
                    config['-target'] = url
            else:
                try:
                    config[op] = int(args[val_i])
                except ValueError:
                    print color('Invalid value for argument: ', 'RED') + op
                    print use.set

    elif args[0] == 'spider':
        if len(args) < 2:
            ######## print use.set
            return
        global queue
        if args[1] == 'start':
            # Initializing new attack queue structure
            queue = fuzz_thread.DictQueue({config.get('-target')
                                          :config.get('-depth')})
            queue.delay = config['-delay'] / 1000.0 # millisec to sec
            # Creating 'n' asynchronous threads
            for i in range(config.get('-threads')):
                th = threading.Thread(name='spider_thread'+str(i), 
                     target=fuzz_thread.spider_thread, args=(queue,))
                th.daemon = True
                th.start()
        elif args[1] == 'stop':
            queue.spider_continue = False
        else:
            pass
            #####

    elif args[0] == 'status':
        print '\n=== ' + color('Spider settings','YELLW') + ' ==='
        print color('Target:  ', 'RED') + config.get('-target')
        print color('Threads: ', 'RED') + str(config.get('-threads'))
        print color('Depth:   ', 'RED') + str(config.get('-depth'))
        print color('Delay:   ', 'RED') + str(config.get('-delay'))
        if queue != None:
            print (color('Links Visited: ', 'BLUE') + 
            str(len(queue.visited_links)))
        print '=======================\n'

       

def print_help():
    _ = '   '
    print '\n=== ' + color('Commands','YELLW') + ' ==='
    print _ + color('help','YELLW') + ' - print this message.'
    print _ + color('exit','YELLW') + ' - exit this terminal.'
    print _ + color('status','YELLW') + ' - show config values and ' \
              'status of jobs. '
    print _ + color('info','YELLW') + color(' job_name', 'GREEN') \
            + ' - show info about a job.'
    print _ + color('set', 'YELLW') + ' - set certain configuration values.'
    print _ + color('spider', 'YELLW') \
            + ' - extract all the links from the target'
    print '================\n'


def color(text, colorStr):
    return col_d[colorStr] + text + col_d['ENDC']


if __name__ == '__main__':
    main(sys.argv)
