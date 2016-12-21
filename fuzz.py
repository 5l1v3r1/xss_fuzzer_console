#!/usr/bin/env python

# import modules
import httplib

# Gather our code in a main() function
def main(url, path):
    conn = httplib.HTTPSConnection(url)
    conn.request("GET", path)
    rsp = conn.getresponse()
    print rsp.status, rsp.reason
    dadta = rsp.read()
    print dadta
    conn.close()

if __name__ == '__main__':
    url = 'resources.allsetlearning.com' 
    path = '/chinese/grammar/'
    main(url, path)
