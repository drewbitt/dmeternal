import unittest
import sys
import os
import pygame
from game.campaign import *
from game import campaign
from game import narrator

class TestClass:
    def test_randomCampaign(self):
        init = narrator.plots.PlotState(rank=1)
        nart = narrator.Narrative( campaign.Campaign(xp_scale=0.25), init, adv_type="STUB_ENDLESS" )
        if nart.story:
            nart.build()
            camp = nart.camp
            pcs = campaign.Random_party()
            if pcs:
                print("\nRandom party allocated; Adding to campaign...")
                camp.add_party(pcs)
                assert pcs == camp.party # Check that the parties are actually the same