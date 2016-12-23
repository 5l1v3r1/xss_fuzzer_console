#!/usr/bin/env python

# import modules
import httplib
import urllib2
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    links = {}
    base_url = ""
    base_path = ""

    @staticmethod
    def is_absolute(url) :
        new_url = ""
        tok = url.split("//")
        if tok[0] == "https:" or tok[0] == "http:":
            new_url = ''.join(tok[1:])
            return True
        else :
            return False
   
    @staticmethod
    def remove_path(url) :
        new_url = ""
        path = ""
        tok = url.split("//")
        if tok[0] == "https:" or tok[0] == "http:":
            new_url = ''.join(tok[1:])
        
        path_tok = new_url.split('/')
        new_url = '//'.join((tok[0], path_tok[0]))
        
        if len(path_tok) > 1 :
            path = '/' + '/'.join(path_tok[1:])

        return (new_url, path)

    def set_target(self, url) :
        ret = self.remove_path(url)
        self.base_url = ret[0]
        self.base_path = ret[1]

    def handle_starttag(self, tag, attrs):
      valid = False    # is url valid
      relative = True # is link relative url addressing
     
      # If tag is a link
      if tag == "a":
        for name, value in attrs:
          # Webpage link
          if name == "href":
            value = value.encode('ascii', 'ignore')
            base  = value # Copy of value that will be modified
            

            # If link changed, then address is absolute
            if self.is_absolute(base) : relative = False
 
            # Extrapolate base url to determine if url is in scope
            if not relative :
              base = self.remove_path(base)[0]
              if base == self.base_url :
                valid = True
            
            # If address begins with '/' it's relative to base url
            # Otherwise address is relative to base + path url
            else :
              valid = True # Relative will usually be valid
              if value[0] != '/':
                value = self.base_url + self.base_path + value
              else :
                value = self.base_url + value
              
            if valid:
                self.links.update({value : 0})
                
# Set attack target. Make connection to ensure valid target
def set_target(request) : 
    connfd = None
    ret = 'Success'
    try:
        connfd = urllib2.urlopen(request)
        connfd.close()
    except urllib2.HTTPError, e:
        ret = 'HTTPError: ' + str(e.code)
    except urllib2.URLError, e:
        ret = 'URLError: ' + str(e.reason)
    except httplib.HTTPException, e:
        ret = 'HTTPException'
    except Exception:
        ret = 'Invalid Target -- Make sure the complete URL is provided'
    return ret

def get_links(url) :
    r = urllib2.urlopen(url)
    data = r.read()
    parser = MyHTMLParser()
    parser.set_target(url)
    parser.feed(data)
    parser.close()
    return parser.links

# Gather our code in a main() function
def main(url, path):
    get_links(url + path)

if __name__ == '__main__':
    url = 'https://resources.allsetlearning.com' 
    path = '/chinese/grammar/'
    main(url, path)
