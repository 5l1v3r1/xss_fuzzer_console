#!/usr/bin/env python

import httplib
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup

"""
Module using BeautifulSoup to establish connection
and parse_html

"""


def parse_html(target, data, depth):
    """
    Method to parse an html for links and forms

    :param target: Target URL to set the scope for parsing
    :param data: HTML data to parse
    :param depth: Within the scope, depth limits how many 
     extra paths can be taken
    :type target: string url
    :type data: string html data
    :return: links dict with structure {url : depth}
    :rtype: string, int

    """

    soup = BeautifulSoup(data, 'html.parser')
    o = urlparse(target)
    scheme = o.scheme  # Http or Https
    base_url = o.netloc  # base url (www. -> .com)
    base_path = o.path   # file path following netloc
    links = {}            # dict of valid links

    # Parse <a> tags
    for link in soup.find_all('a'):
        valid = False     # is url valid
        relative = False  # is link relative url addressing
        value = link.get('href')  # link url
        if value == None:
            continue

        o = urlparse(value)
        if o.netloc == '':
            relative = True  # default is False

        # Check if absolute URL is in scope
        if not relative:
            if o.netloc == base_url:
                valid = True
        # If address begins with '/' it's relative to base url
        # Otherwise address is relative to base + path url
        else:
            valid = True  # Relative will usually be valid
            if value[0] != '/':  # Start from target dir
                value = scheme + '://' + base_url + base_path + value
            else:               # Start from root dir
                value = scheme + '://' + base_url + value
        if valid:
            links.update({value: depth})

    # Parse all forms
    for form in soup.find_all('form'):
        value = scheme + '://' + base_url + base_path
        # if form.get('method') != 'GET': # Only parse GET requests
        #    continue;

        action = form.get('action')
        if action:
            value = value + action

        inputs = form.find_all('input')  # List of inputs for form
        if not inputs:
            continue

        # O(n^2), but there will usually only be 1 or 2 inputs
        for input in inputs:
            name = input.get('name')
            if name:
                value = value + '?' + name + '=abc'
        links.update({value: depth})
        # print value
    return links


def set_target(request):
    """
    Set attack target. Makes connection to ensure that target is valid.

    Args:
        request: The target url to connect with

    Returns:
        A tuple of connection file and a string response. The connfd is file object that contains meta data to be used by the scraper. The string response indicates whether the connection was successful or an exception was caught.

    """
    connfd = None
    ret = 'Success'
    try:
        connfd = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        ret = 'HTTPError: ' + str(e.code)
    except urllib2.URLError, e:
        ret = 'URLError: ' + str(e.reason)
    except httplib.HTTPException, e:
        ret = 'HTTPException'
    except Exception:
        ret = 'Invalid Target -- Make sure the complete URL is provided'
    return connfd, ret

# Find all of the links in the connection response for a given url


def scrape_links(url, depth):
    """

    """
    target = set_target(url)
    conn = target[0]
    result = target[1]

    if result != 'Success':
        return None

    # Don't want to parse a plaintext file
    encoding = conn.headers.getparam('charset')
    content = conn.info().type
    if content == 'text/plain':
        return None
    # TODO Consider handling different content types
    # Retrieve connection response
    data = conn.read()

    # Decode if necessary
    if encoding != None:
        data = data.decode(encoding)

    # Parse html response
    links = parse_html(url, data, depth - 1)
    # print len(links)
    return (links, data)  # links in the data + the data itself

# Connect to a url and return the data


def get_data(url):
    """

    """
    target = set_target(url)
    conn = target[0]
    result = target[1]
    if result != 'Success':
        return None
    return conn.read()
