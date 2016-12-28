#!/usr/bin/env python

# import modules
import httplib
import urllib2
from urlparse import urlparse
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    links = {}
    scheme = "" # url scheme such as http or https
    base_url = ""
    base_path = ""
    depth = 0

    def set_target(self, url) :
        # Parsing target url with urlparse library
        o = urlparse(url)
        self.scheme = o.scheme
        self.base_url   =  o.netloc 
        self.base_path  = o.path   

    def handle_starttag(self, tag, attrs):
      valid = False    # is url valid
      relative = False # is link relative url addressing
     
      # If tag is a link
      if tag == "a":
        for name, value in attrs:
          # Webpage link
          if name == "href":
            #//value = value.encode('ascii', 'ignore')
            
            o = urlparse(value)
            if o.netloc == '' : 
                relative = True # default is False

            # Check if absolute URL is in scope
            if not relative :
                if o.netloc == self.base_url :
                    valid = True
            # If address begins with '/' it's relative to base url
            # Otherwise address is relative to base + path url
            else :
                valid = True # Relative will usually be valid
                if value[0] != '/':
                    value = (self.scheme + '://' + self.base_url + 
                             self.base_path + value)
                else :
                    value = self.scheme + '://' +  self.base_url + value
              
            if valid:
                self.links.update({value : self.depth})
                
# Set attack target. Make connection to ensure valid target
def set_target(request): 
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

def scrape_links(url, depth):
    target = set_target(url)
    conn = target[0]
    result = target[1]

    if result != 'Success':
        return None

    encoding = conn.headers.getparam('charset')
    content = conn.info().type 
    if content == 'text/plain':
        return None

    data = conn.read()
    
    if encoding != None:
        data = data.decode(encoding)

    parser = MyHTMLParser()
    parser.depth = depth - 1
    parser.set_target(url)
    parser.feed(data)
    parser.close()
    return parser.links

# Gather our code in a main() function
def main(url, path):
    scrape_links(url + path)

if __name__ == '__main__':
    url = 'https://resources.allsetlearning.com' 
    path = '/chinese/grammar/'
    main(url, path)
