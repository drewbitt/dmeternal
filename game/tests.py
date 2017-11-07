import unittest
from __init__ import main
#import __init__

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertRaises(Exception, main())

if __name__ == '__main__':
    #game = main()
    unittest.main()