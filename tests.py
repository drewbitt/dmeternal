import unittest
import game
#import __init__

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertRaises(Exception, game.main())

if __name__ == '__main__':
    #game = main()
    unittest.main()