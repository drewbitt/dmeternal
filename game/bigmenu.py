
import rpgmenu
import pygwrap
import image
import pygame

class ViewDrawer ( pygame.Rect ):
    ''' Re-implemented one of the charsheet classes to work for the BigMenu. Combined with
    rpgmenu, gives us our menu.
    '''

    ''' My idea:
    I want to quit in here. I want to set settings in here, like frames per second that the settings file has.
    Other settings can go here
    I want a checkbox that says Dev Console. If checked, the bottom portion of this menu becomes an active
    dev console terminal
    '''

    '''Problems with current approach:
    * Would have to add items to RPGMenu, like checkboxes etc that we would want to use for settings.
        Suggestion: at least use a dev console file for that rpgmenu item, can add others
    * It is currently using mymenu.add_alpha_keys() and mymenu.query() to get the menu to stay up. That was my biggest issue.
      We probably will not be needing input like a,b,c etc. like a normal menu, so need to implement this ourselves.
      Basically, a large overhaul / additions to rpgmenu is needed
    '''

    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.
    WIDTH = 800
    HEIGHT = 650

    def __init__( self, x=0, y=0, screen = None ):
        x = screen.get_width() // 2 - (self.WIDTH / 2)
        y = screen.get_height() // 2 - self.HEIGHT // 2 + 32
        super(ViewDrawer, self).__init__(x,y,self.WIDTH,self.HEIGHT)
        self.render_permanent_stuff(screen)

    def just_print_example( self, screen, x, y, text1, text2, width=120, color=pygwrap.TEXT_COLOR ):
        """Do proper justification for stat line at x,y.
        Just an example of how to print."""
        if text1:
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, text1, pygame.Rect( x, y, width, 20 ), justify = -1, color=color )
        if text2:
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, text2, pygame.Rect( x, y, width, 20 ), justify = 1, color=color )

    def render_permanent_stuff(self, screen):
        pygwrap.default_border.render( screen , self )
        self.just_print_example(screen, self.x + 6, self.y+10, "EYY", "")


class ActualMenu (rpgmenu.Menu):
    ''' Class that is a child of rpgmenu, meaning you can add menu items to it '''
    def __init__( self, screen, predraw = None, border=None ):
        x = screen.get_width() // 2 - (ViewDrawer.WIDTH / 2)
        y = screen.get_height() // 2 - ViewDrawer.HEIGHT // 2 + 40 + pygwrap.BIGFONT.get_linesize() * 2
        super(ActualMenu, self).__init__(screen,x,y,ViewDrawer.WIDTH,ViewDrawer.HEIGHT - pygwrap.BIGFONT.get_linesize() * 2, border=border)
        self.predraw = predraw

class ViewReDrawer( object ):
    ''' Class that redraws the view whenever it is updated, like the user changing active menu item. Adds a permanent caption section. view=the main ViewDrawer'''
    def __init__( self, border_rect=None, backdrop="bg_wests_stonewall5.png", menu=None, view=None, screen=None, caption=None, predraw=None ):
        self.backdrop = image.Image( backdrop )
        self.counter = 0
        self.view = view

        if screen and not border_rect:
            border_rect = pygame.Rect( screen.get_width()//2 + 64, screen.get_height()//2 - ViewDrawer.HEIGHT//2 + 32, ViewDrawer.WIDTH - 64, ViewDrawer.HEIGHT )
        self.rect = border_rect
        if screen:
            self.caption_rect = pygame.Rect( screen.get_width()//2 - 240, screen.get_height()//2 - ViewDrawer.HEIGHT//2 - 46, 480, pygwrap.BIGFONT.get_linesize() )
        else:
            self.caption_rect = None

        self.caption = caption
        self.menu = menu
        self.predraw = predraw

    def __call__( self , screen ):
        if self.predraw:
            self.predraw( screen )
        else:
            self.backdrop.tile( screen , ( self.counter * 5 , self.counter ) )

        if self.view:
            self.view.render_permanent_stuff( screen )

        if self.caption and self.caption_rect:
            pygwrap.default_border.render( screen , self.caption_rect )
            pygwrap.draw_text( screen, pygwrap.BIGFONT, self.caption, self.caption_rect, justify = 0 )
        self.counter += 4
