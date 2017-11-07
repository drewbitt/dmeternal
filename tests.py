import unittest
import game
import pygame
import pygwrap
#from __init__ import main
#import __init__

def createCampaign(self):
        pygame.init()
        screen = pygame.display.set_mode( (800,600) )
        pygwrap.init()
        rpgmenu.init()
        camp = campaign.Campaign()
        for t in range( 100 ):
            nart = narrator.Narrative( camp, narrator.plots.PlotState(rank=t%5+1), adv_type="SHORTIE",start_rank=t%5+1, end_rank=5 )
            #nart.build()
            print t

        for p in narrator.UNSORTED_PLOT_LIST:
            if p._used > 0:
                print "{} [{}]".format( p, p._used )

class TestMethods(unittest.TestCase):
    def test_createCampaign(self):
        self.assertRaises(Exception, createCampaign(self))

if __name__ == '__main__':
    unittest.main()