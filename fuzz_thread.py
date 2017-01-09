#!/usr/bin/env python

# import modules
from urlparse import urlparse, parse_qs, ParseResult
from attack import AttackURL, AttackContext
import threading
import connect 
import time
import util
import sys
import re

# Synchronized Ordered Dictionary that serves as a queue
class DictQueue:
    attack_running = True # Should attacking threads continue
    spider_running = True # Should spider threads continue
    delay = 0 
    queue_size = 0
    cv = threading.Condition()
    cv_atk = threading.Condition() # CondVar for attack threads
    timer_lock = threading.Lock()
    dict_queue = dict()     # Links not yet visited
    visited_links = dict()  # Dictionary of visiteed links
    param_atk = list()     # list of param urls as attack objects
    param_links = set()    # list of original param urls

    # Adding initial target link
    def __init__(self, link):
        self.add_links(link)
    
    # Get URL for purposes of spidering
    def get_link(self):
        #TODO set timeout
        self.cv.acquire()
        while not len(self.dict_queue):
            self.cv.wait()
       
        item = self.dict_queue.popitem()             # pop from queue
        self.visited_links.update({item[0]:item[1]}) # add to visited dir
        self.cv.release()
        return item

    # Get Attack Obj for purposes of attacking 
    def get_attack_obj(self):
        self.cv_atk.acquire()
        while not len(self.param_links):
            self.cv.wait()
       
        atk_obj = self.param_atk.pop()   # pop from queue
        self.cv_atk.release()
        return atk_obj # Return AttackURL object 

    # Add attack objects to param_atk list
    def add_attack_objects(self, objects):
        self.cv_atk.acquire() # Mutex to ensure atomic queue modification
        url = objects[0]
        atk_objs = objects[1]
        # Checking for duplicates, then adding to queue
        if url in self.param_links: # Already added links
            return
        else:
            self.param_links.add(url)
            self.param_atk.extend(atk_objs) # Extend, then sort 
            self.param_atk.sort(key=lambda x: x.attempt_cnt,
                                reverse = True)
        #for _ in atk_objs:
        #    print _.attempt_cnt

        self.cv_atk.notifyAll()
        self.cv_atk.release()

    # Links added en-masse to avoid constant synch procedure calls
    def add_links(self, links): # links represented as a dictionary
        self.cv.acquire()
        # upload links
        for url, depth in links.items():
            # Reference visited links
            if depth == -1: # If recursive limit is reached
                continue

            # Checking if link has parameters
            parse = urlparse(url)
            params = parse_qs(parse.query.encode('utf-8')) 
            if params: # If params, create attack object
                # Create Attack Object List
                atk_objs = AttackURL.create(self, parse, params)
                obj = url, atk_objs
                self.add_attack_objects(obj) # Add objects to queue

            # Avoid repeats if at same or lower depth 
            q_depth = self.dict_queue.get(url, -1)
            v_depth = self.visited_links.get(url, -1)
            if depth <= q_depth or depth <= v_depth:
                continue
            
            # Adding to unvisited links queue
            self.dict_queue.update({url: depth})
        
        self.cv.notifyAll()
        self.cv.release()

    # Provides thread-safe delayed connection, if necessary
    def delay_conn(self, link):
        if self.delay != 0: # Only one request per delay interval 
            self.timer_lock.acquire()
            time.sleep(self.delay)
            self.timer_lock.release()
        
        # Time of connection is not included in the delay
        return connect.scrape_links(link[0], link[1])
    
    # Provides thread-safe delayed connection. Returns the html response
    def delay_conn_data(self, url):
        if self.delay != 0: # Only one request per delay interval 
            self.timer_lock.acquire()
            time.sleep(self.delay)
            self.timer_lock.release()
        
        # Time of connection ias not included in the delay
        return connect.get_data(url)

# Function executed by spider threads
def spider_thread(queue):
    while queue.spider_running:
        # Retrieve URL and make connection
        link = queue.get_link()
        response = queue.delay_conn(link)

        if response == None: continue
        link_dict = response[0]
        data = response[1]
       
        # Storing data in attack object if visited parameterized url
        #param_obj = queue.param_links.get(link[0]) 
        #if param_obj != None:   
        #    param_obj.set_data(data)
        #    param_obj.init_context()
        # Adding discovered links to queue
        queue.add_links(link_dict)


# Function executed by attack threads
def attack_thread(queue):
    print 'attack thread'
    if queue == None:
        return

    while queue.attack_running:
        # Retrieve URL and make attack procedure call
        obj = queue.get_attack_obj()
        success = obj.attack() 
        if success:
            pass # Readd if successful (Nothing went wrong)




