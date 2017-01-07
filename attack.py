#!/usr/bin/env python
from urlparse import urlparse, parse_qs, ParseResult
from urllib import urlencode
from collections import OrderedDict
import os, binascii
import random
import string
import util

# Class containing necessary metadata for each attack vector
class AttackContext:
    # Context essentially refers to the attack location 
    queue = None       # Make DictQueue object
    cookie = ''        # Inserted cookie to find
    data = ''          # Raw HTML

    # Initial data parsing variables
    tag = ''           # Direct Parent Tag
    tag_closed = False # Has the open parent tag been closed
    is_js = False      # In a javascript context
    in_value = True    # Has iteration passed the assignment
    delimiter = ''     # Is the input encapsulated by ' or "
    key = ''           # identifier for context and attack string

    # Filter Fuzzing variables
    fuzz_str = ''      # String containing current fuzzer attack
    attack_str = ''    # String demonstrating successful attack
    attempt_cnt = 0    # Current number of attempts

    '''
    f - filter avoidance dictionary
    Value is a tuple of (attack_char, passed_filter ) where passed
    filter means that it successfuly reflected onto the page '''
    f = OrderedDict()

    # Initialize class variables and parse current context
    def __init__(self, data, cookie, pos):
        self.data = data
        self.cookie = cookie
        self.key = gen_key()


        d = 0 # Distance from initial pos
        for i in reversed(data[0:pos]):
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

        self.set_target_chars() # Identify fuzzer characters
        self.make_fuzz_str()    # Construct fuzzer string

    # Set the Parent tag for the current context
    def set_tag(self, start, end):
        # Split using space as delimiter
        no_space = self.data[start:end].split(' ')
	tag = no_space[0]
        
        # If tag is closed, make sure closing tag isn't included
        if self.tag_closed:
            tag = tag.split('>')[0]
        
        self.tag = tag # Tag set

    # Determine necessary characters for escape
    def set_target_chars(self):
        if self.delimiter != '':
            self.f.update({self.delimiter:self.delimiter})
        
        if self.tag_closed: # Inside of tag content section
            # Need chars: < / > script
            self.f.update({'<':('<',
                           '/':'/',
                           '>':'<',
                           'script':'script'})
        else: # Desired objective is to introduce new attr
            # TODO for these you don't need to escape completely, you
            # can instead just introduce a new attribute like onerror

        if self.is_js:
            self.f.update({';':';'})
            print 'JS_CONTEXT --set_target_chars'
    
    def make_fuzz_str(self):
        fuzz = self.cookie 
        print 'fuzz begin ' + fuzz
        for char in self.f.values():
            fuzz += self.key
            fuzz += char

    def fuzz_context(self):
        

# Class containing Attack URLs with their associated metadata
class AttackURL:
    queue = None # DictQueue object
    cookie = str(binascii.b2a_hex(os.urandom(2))) # Generate cookie
    url = ''
    visited = False
    data = '' # html data
    atk_vectors = list() # attack vectors -- list of AttackContext's

    def __init__(self, queue, url):
        self.queue = queue
        self.url = url

    def set_data(self, data):
        self.data = data
        visited = True

    def init_context(self):
        if self.data == '':
            return None

        # Find all cookie reflections in the HTML
        match = util.string_match(self.data, self.cookie)
        for pos in match:
            context = AttackContext(self.data, self.cookie, pos)

    # Generates an attack object for parameterized URLs
    @staticmethod
    def create(queue, parsed_url, params):
        p = parsed_url
        # Changing each argument value to the cookie
        for param, value in params.items(): 
            params[param] = AttackURL.cookie
        new_params = urlencode(params, doseq=True)
        new_url = ParseResult(p.scheme, p.netloc, p.path, p.params,
                new_params, p.fragment).geturl()

        return AttackURL(queue, new_url) # Return new attack object

    def attack(self):
        pass

# Generate random two character key
def gen_key():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
