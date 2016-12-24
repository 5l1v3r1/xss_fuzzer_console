#!/usr/bin/env python

# import modules
import threading
import collections
import fuzzer 
import copy

FIFO = False # Constant for OrderedDict

# rename get_links to scrape_link
# TODO synchronize scrape_link around a timer 

# Synchronized Ordered Dictionary that serves as a queue
class DictQueue:
    queue_size = 0
    cv = threading.Condition()
    dict_queue = collections.OrderedDict()
    visited_links = dict()

    # Adding initial target link
    def __init__(self, link):
        self.add_links(link)

        
    def get_link(self):
        # set timeout
        self.cv.acquire()
        while not len(self.dict_queue) :
            self.cv.wait()
        self.queue_size -= 1
       
        item = self.dict_queue.popitem(FIFO) # pop from queue
        self.visited_links.update({item[0]:item[1]}) # add to visited dir
        self.cv.release()

        return item[0]

    # Links added en-masse to avoid constant synch procedure calls
    def add_links(self, links): # links represented as a dictionary
        self.cv.acquire()
        # upload links
        for key, value in links.iteritems() :
            # TODO be more restrictive, only update if necessary
            # Reference visited links
            self.dict_queue.update({copy.copy(key) : copy.copy(value)})

        self.cv.notifyAll()
        self.cv.release()

def spider_thread(queue):
    url = queue.get_link()
    link_dict = fuzzer.get_links(url)
    queue.add_links(link_dict)
    #print 'URL: ' + url + '   LEN: ' + str(len(queue.dict_queue))
