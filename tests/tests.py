import unittest
import sys
import os
import pygame
sys.path.append('../')
from game.campaign import *
from game import campaign
from game import narrator
from game import rpgmenu
from game import characters
from game.characters import *
from game.__init__ import load_campaign_no_play

class TestClass:
	def test_characterGen(self):
		flag = True
		init = narrator.plots.PlotState(rank=1)
		nart = narrator.Narrative( campaign.Campaign(xp_scale=0.65), init, adv_type="STUB_ENDLESS" )
		if nart.story:
			nart.build()
			camp = nart.camp
			pcs = campaign.Random_party()
			if camp.num_pcs() > 0:
				if not camp.first_living_pc():
					flag = False
			assert flag == True

	# Disabled until file reference issues are fixed
	#def test_loadCampaign(self):
	#	os.environ["SDL_VIDEODRIVER"] = "dummy"
	#	pygame.init()
	#	screen = pygame.display.set_mode( (1920,1080), pygame.FULLSCREEN )
	#	pygwrap.init()
	#	rpgmenu.init()
	#	assert load_campaign_no_play(screen) == True

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

	def test_explorer(self):
		print("\nBeginning Explorer Test...")
		os.environ["SDL_VIDEODRIVER"] = "dummy"
		pygame.init()
		screen = pygame.display.set_mode( (1920,1080), pygame.FULLSCREEN )
		pygwrap.init()
		rpgmenu.init()
		
		# create campaign
		init = narrator.plots.PlotState(rank=1)
		pygwrap.please_stand_by( screen, "Building world..." )
		nart = narrator.Narrative( campaign.Campaign(xp_scale=0.25), init, adv_type="STUB_ENDLESS" )
		if nart.story:
			nart.build()
			camp = nart.camp
			pcs = campaign.Random_party()
			if pcs:
				camp.add_party( pcs )
				camp.place_party()
				print("\nCreating Explorer...")
				exp = exploration.Explorer( screen, camp )
				assert exp.camp == camp			
	