import unittest
from connect import set_target, scrape_links

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_connect(self):
        res = set_target('https://www.google.com/')[1]
        self.assertEquals(res, 'Success')
    
    def test_scrape(self):
        res = scrape_links('https://www.google.com/', 3)
        self.assertTrue(res != None)


if __name__ == '__main__':
    unittest.main()




