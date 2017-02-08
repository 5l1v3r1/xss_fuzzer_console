import unittest
import fuzz_thread
from connect import set_target, scrape_links, parse_html


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    # Test connection success
    def test_connect(self):
        res = set_target('https://www.google.com/')[1]
        self.assertEquals(res, 'Success')

    # Test basic scraper functionality
    def test_scrape(self):
        res = scrape_links('https://www.google.com/', 3)
        self.assertTrue(res != None)

    # Test scraper parsing ability
    def test_scrape_2(self):
        data = open('test_html/wiki.dat').read()
        url = 'https://en.wikipedia.org/wiki/George_Frideric_Handel'
        link_cnt = 861 
        length = len(parse_html(url, data, 10))
        self.assertEquals(link_cnt, length)

    # Test queue class, and see if discovering paramaterized urls
    def test_queue(self):
        data = open('test_html/wiki.dat').read()
        url = 'https://en.wikipedia.org/wiki/George_Frideric_Handel'
        links = parse_html(url, data, 10)
        queue = fuzz_thread.DictQueue({url: 5})
        queue.delay = 0
        queue.add_links(links)
    
        # 30 parameterized links in the html
        self.assertEquals(len(queue.param_links), 30)

if __name__ == '__main__':
    unittest.main()
