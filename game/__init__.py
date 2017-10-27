# -*- coding: utf-8 -*-
#       
#       Copyright 2014 Joseph Hewitt <pyrrho12@yahoo.ca>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
# 

import narrator
import context
import maps
import pygame
import pygwrap
import rpgmenu
import campaign
import util
import cPickle
import image
import glob
import random
import chargen
import charloader
import sys
import os

VERSION_ID = "0.5.0 Alpha"

set_xp = 0.65

class PosterRedraw( object ):
    def __init__( self, screen ):
        self.image = pygame.image.load( random.choice( pygwrap.POSTERS ) ).convert()
        self.image_dest = self.image.get_rect( center=(screen.get_width()//2,screen.get_height()//2) )
    def __call__( self, screen ):
        screen.fill( (0,0,0) )
        screen.blit(self.image , self.image_dest )

class TitleScreenRedraw( object ):
    def __init__( self, screen ):
        self.screen_center_x = screen.get_width() // 2
        self.screen_center_y = screen.get_height() // 2
        self.logo = image.Image( "sys_logo.png" )
        self.logo_dest = self.logo.bitmap.get_rect( midbottom=(self.screen_center_x,self.screen_center_y-25) )
        self.version = pygwrap.ITALICFONT.render( VERSION_ID, True, pygwrap.TEXT_COLOR )
        self.version_dest = self.version.get_rect( midtop = self.logo_dest.midbottom )
        self.get_bg_image()

    def get_bg_image( self ):
        self.image = pygame.image.load( random.choice( pygwrap.POSTERS ) ).convert()
        self.image_dest = self.image.get_rect( center=(self.screen_center_x,self.screen_center_y) )

    def __call__( self, screen ):
        screen.fill( (0,0,0) )
        screen.blit(self.image , self.image_dest )
        screen.blit(self.logo.bitmap , self.logo_dest )
        screen.blit(self.version , self.version_dest )

def choose_characters( screen ):
    rpm = rpgmenu.Menu( screen,screen.get_width()//2-100,screen.get_height()//2 + 25,200,200,predraw=None )
    rpm.add_item( "Load Characters", True )
    rpm.add_item( "Random Party", False )
    if rpm.query():
        return charloader.load_characters( list(), screen )
    else:
        return campaign.Random_party()

def start_campaign( init, screen ):
    pygwrap.please_stand_by( screen, "Building world..." )
    nart = narrator.Narrative( campaign.Campaign(), init )
    if nart.story:
        nart.build()
        camp = nart.camp
        pcs = choose_characters( screen )
        if pcs:
            camp.name = pygwrap.input_string(screen, redrawer=PosterRedraw(screen), prompt="Enter campaign name" )
            camp.add_party( pcs )
            camp.place_party()
            camp.play( screen )

def default_start_campaign( screen ):
    start_campaign( narrator.plots.PlotState(rank=1), screen )

def bardic_start_campaign( screen ):
    init = narrator.plots.PlotState(rank=1)
    pygwrap.please_stand_by( screen, "Building world..." )
    nart = narrator.Narrative( campaign.Campaign(), init, adv_type="STUB_BARDIC", end_rank=5 )
    if nart.story:
        nart.build()
        camp = nart.camp
        pcs = choose_characters( screen )
        if pcs:
            camp.name = pygwrap.input_string(screen, redrawer=PosterRedraw(screen), prompt="Enter campaign name" )
            camp.add_party( pcs )
            camp.place_party()
            camp.play( screen )

def endless_start_campaign( screen ):
    global set_xp
    init = narrator.plots.PlotState(rank=1)
    pygwrap.please_stand_by( screen, "Building world..." )
    nart = narrator.Narrative( campaign.Campaign(xp_scale=set_xp), init, adv_type="STUB_ENDLESS" )
    if nart.story:
        nart.build()
        camp = nart.camp
        pcs = choose_characters( screen )
        if pcs:
            camp.add_party( pcs )
            camp.place_party()
        camp.name = pygwrap.input_string(screen, redrawer=PosterRedraw(screen), prompt="Enter campaign name" )
        camp.play( screen )


def load_campaign( screen ):
    rpm = rpgmenu.Menu( screen,screen.get_width()//2-250,screen.get_height()//2-50,500,100,predraw=PosterRedraw(screen) )
    rpm.add_files( util.user_dir("rpg_*.sav") )
    rpm.sort()
    rpm.add_alpha_keys()
    rpm.add_item( "Cancel Load Campaign", None )
    cmd = rpm.query()
    if cmd:
        pygwrap.please_stand_by( screen, "Loading..." )
        with open( cmd, "rb" ) as f:
            camp = cPickle.load( f )
        if camp:
            camp.play( screen )

def test_campaign_generator( screen ):
    camp = campaign.Campaign()
    for t in range( 100 ):
        nart = narrator.Narrative( camp, narrator.plots.PlotState(rank=t%5+1), adv_type="SHORTIE",start_rank=t%5+1, end_rank=5 )
        #nart.build()
        print t

    for p in narrator.UNSORTED_PLOT_LIST:
        if p._used > 0:
            print "{} [{}]".format( p, p._used )


def toggle_fullscreen_default( screen ):
    scrsize = width,height = 600,400
    fullscreen_sz = pygame.display.Info().current_w, pygame.display.Info().current_h
    win_pos_left = 1 + ((fullscreen_sz[0] - width) // 2)
    win_pos_top = 1 + ((fullscreen_sz[1] - height) // 2)
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{0},{1}'.format(win_pos_left, win_pos_top) #reset enviroment varibles

    if util.config.getboolean( "DEFAULT", "fullscreen"): #checks fullscreen in config.cfg
        util.config.set( "DEFAULT", "fullscreen", "False") #changes fullscreen in config.cfg buffer
        pygame.display.set_mode((800,600)) #change current display flag
    else:
        util.config.set( "DEFAULT", "fullscreen", "True")
        pygame.display.set_mode((800,600),pygame.FULLSCREEN)
    #write changes in config.cfg to file
    with open( util.user_dir( "config.cfg" ) , "wb" ) as f:
        util.config.write( f )
    #update display with new flags
    pygame.display.update()

    return 0


def load_settings( screen ):
    rpm = rpgmenu.Menu( screen,screen.get_width()//2-250,screen.get_height()//2-50,500,100,predraw=PosterRedraw(screen) )
    rpm.sort()
    rpm.add_alpha_keys()
    rpm.add_item("Fullscreen (on/off)", toggle_fullscreen_default )
    rpm.add_item( "Enable Dev Console", None )
    rpm.add_item( "Difficulty Settings", difficulty_settings)
    rpm.add_item( "Back", None)
    cmd = rpm.query()
    cmd = True
    while cmd:
        cmd = rpm.query()
        if cmd:
            cmd( screen )
        if pygwrap.GOT_QUIT:
            break

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
def difficulty_settings( screen ):
    global set_xp
    rpm = rpgmenu.Menu(screen, screen.get_width() // 2 - 250, screen.get_height() // 2 - 50, 500, 100,
    predraw=PosterRedraw(screen))
    rpm.sort()
    rpm.add_alpha_keys()
    rpm.add_item("Easy", 1)
    rpm.add_item("Normal(default)", 2)
    rpm.add_item("Hard", 3)
    rpm.add_item("Endless", 4)
    rpm.add_item("Check setting", 5)
    rpm.add_item("Back", None)
    cmd = rpm.query()
    if cmd == 1:
        set_xp = 0.8
    elif cmd == 2:
        set_xp = 0.65
    elif cmd == 3:
        set_xp = 0.4
    elif cmd == 4:
        set_xp = 0.25
    elif cmd == 5:
        check_difficulty(screen)

def check_difficulty( screen ):
    rpm = rpgmenu.Menu(screen, screen.get_width() // 2 - 250, screen.get_height() // 2 - 50, 500, 100,
    predraw=PosterRedraw(screen))
    rpm.sort()
    rpm.add_alpha_keys()
    global set_xp
    init = narrator.plots.PlotState(rank=1)
    nart = narrator.Narrative(campaign.Campaign(xp_scale=set_xp), init, adv_type="STUB_ENDLESS")
    if nart.story:
        nart.build()
    difficulty_type = nart.camp.get_difficulty(set_xp)
    rpm.add_item(difficulty_type, None)
    rpm.add_item("Back", None)
    cmd = rpm.query()
    cmd = True
    while cmd:
        cmd = rpm.query()
        if cmd:
            cmd(screen)
        if pygwrap.GOT_QUIT:
            break

=======
>>>>>>> 1f53b755f371019156c7ed754aa9373bca3cdffc
>>>>>>> Stashed changes
def main():
    pygame.init()
    pygame.display.set_caption("Dungeon Monkey Eternal","DMEternal")
    pygame.display.set_icon(pygame.image.load(util.image_dir("sys_icon.png")))
    # Set the screen size.
    if util.config.getboolean( "DEFAULT", "fullscreen" ):
        screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
    else:
        screen = pygame.display.set_mode( (800,600) )
    pygwrap.init()
    rpgmenu.init()

    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    rpm = rpgmenu.Menu( screen,screen_center_x-100,screen_center_y + 25,200,200,predraw=TitleScreenRedraw(screen) )

    rpm.add_item( "Create Character", chargen.make_and_save_character )
    rpm.add_item( "Load Campaign", load_campaign )
    rpm.add_item( "Start Endless Campaign", endless_start_campaign )
    #rpm.add_item( "Start Bardic Campaign", bardic_start_campaign )
    #rpm.add_item( "Start Gen1 Campaign", default_start_campaign )
    rpm.add_item( "Browse Characters", campaign.browse_pcs )
    rpm.add_item( "Settings", load_settings)
    #rpm.add_item( "Test Campaign Generator", test_campaign_generator )
    rpm.add_item( "Quit Game", None )

    cmd = True
    while cmd:
        cmd = rpm.query()
        if cmd:
            cmd( screen )
        if pygwrap.GOT_QUIT:
            break

if __name__=='__main__':
    main()


