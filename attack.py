#!/usr/bin/env python
from urlparse import urlparse, parse_qs, ParseResult
from urllib import urlencode
import os, binascii
import util

# Class containing necessary metadata for each attack vector
class AttackContext:
    # Context essentially refers to the attack location 
    cookie = ''        # Inserted cookie to find
    data = ''          # Raw HTML
    tag = ''           # Direct Parent Tag
    tag_closed = False # Has the open parent tag been closed
    is_js = False      # In a javascript context
    in_value = True    # Has iteration passed the assignment
    delimiter = ''     # Is the input encapsulated by ' or "

    # f - filter avoidance dictionary
    f = {"'"  : "'",
         "\"" : "\"",
         ";"  : ";",
         "!"  : "!",
         "<"  : "<",
         ">"  : ">",
         "="  : "=",
         "&"  : "&"}

    # Initialize class variables and parse current context
    def __init__(self, data, cookie, pos):
        self.data = data
        self.cookie = cookie
        d = 0
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

    # Set the Parent tag for the current context
    def set_tag(self, start, end):
        # Split using space as delimiter
        no_space = self.data[start:end].split(' ')
	tag = no_space[0]
        
        # If tag is closed, make sure closing tag isn't included
        if self.tag_closed:
            tag = tag.split('>')[0]
        
        self.tag = tag # Tag set

# Class containing Attack URLs with their associated metadata
class AttackURL:
    cookie = str(binascii.b2a_hex(os.urandom(3))) # Generate cookie
    url = ''
    visited = False
    data = '' # html data
    atk_vectors = list() # attack vectors -- list of AttackContext's

    def __init__(self, url):
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
    def create(parsed_url, params):
        p = parsed_url
        # Changing each argument value to the cookie
        for param, value in params.items(): 
            params[param] = AttackURL.cookie
        new_params = urlencode(params, doseq=True)
        new_url = ParseResult(p.scheme, p.netloc, p.path, p.params,
                new_params, p.fragment).geturl()

        return AttackURL(new_url) # Return new attack object
