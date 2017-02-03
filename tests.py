import unittest
from connect import set_target

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_connect(self):
        self.assertEquals(set_target('https://www.google.com/')[1], 'Success')



if __name__ == '__main__':
    unittest.main()




