#!/usr/bin/env python

# import modules
import threading
import collections
import fuzzer 
import copy
import time

FIFO = False # Constant for OrderedDict

# rename fuzzer file to connect
# rename fuzzerget_links to scrape_link

# Synchronized Ordered Dictionary that serves as a queue
class DictQueue:
    delay = .100
    queue_size = 0
    cv = threading.Condition()
    timer_lock = threading.Lock()
    dict_queue = collections.OrderedDict()
    visited_links = dict()

    # Adding initial target link
    def __init__(self, link):
        self.add_links(link)

        
    def get_link(self):
        # set timeout
        self.cv.acquire()
        while not len(self.dict_queue):
            self.cv.wait()
        self.queue_size -= 1
       
        item = self.dict_queue.popitem(FIFO) # pop from queue
        self.visited_links.update({item[0]:item[1]}) # add to visited dir
        self.cv.release()

        return item

    # Links added en-masse to avoid constant synch procedure calls
    def add_links(self, links): # links represented as a dictionary
        self.cv.acquire()
        # upload links
        for key, depth in links.items():
            # Reference visited links
            if depth == 0: # If recursive limit is reached
                continue

            # Avoid repeats if at same or lower depth 
            q_depth = self.dict_queue.get(key, -1)
            v_depth = self.visited_links.get(key, -1)
            if depth <= q_depth or depth <= v_depth:
                continue

            # TODO check if copying is actually necessary
            self.dict_queue.update({copy.copy(key): copy.copy(depth)})

        self.cv.notify(1)
        self.cv.release()

    # Provides thread-safe delayed connection, if necessary
    def delay_conn(self, link):
        if self.delay != 0: # Only one request per delay interval 
            self.timer_lock.acquire()
            time.sleep(self.delay)
            self.timer_lock.release()
        
        # Time of connection is not included in the delay
        return fuzzer.scrape_links(link[0], link[1])

def spider_thread(queue):
    while 1:
        link = queue.get_link()
        print 'URL: ' + link[0] + '   LEN: ' + str(len(queue.dict_queue))
        
        link_dict = queue.delay_conn(link)
        if link_dict != None:
            queue.add_links(link_dict)




