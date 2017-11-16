import pygame

import image
import pygwrap
import rpgmenu

class ViewDrawer ( pygame.Rect ):
    ''' Re-implemented one of the charsheet classes to work for the BigMenu. Combined with
    rpgmenu, gives us our menu.
    '''

    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.

    # Can create any menu like this of any size by specifying bigmenu.ViewDrawer.HEIGHT = x
    # before creating the ViewRedrawer/Drawer
    WIDTH = 800
    HEIGHT = 650

    def __init__( self, x=0, y=0, screen = None ):
        x = screen.get_width() // 2 - (self.WIDTH / 2)
        y = screen.get_height() // 2 - self.HEIGHT // 2 + 32
        super(ViewDrawer, self).__init__(x,y,self.WIDTH,self.HEIGHT)

    def just_print_example( self, screen, x, y, text1, text2, width=200, color=pygwrap.TEXT_COLOR ):
        """Do proper justification for stat line at x,y.
        Just an example of how to print."""
        if text1:
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, text1, pygame.Rect( x, y, width, 20 ), justify = -1, color=color )
        if text2:
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, text2, pygame.Rect( x, y, width, 20 ), justify = 1, color=color )

    def render_permanent_stuff(self, screen, style, camp=None):
        ''' Render permanent, non-selectable objects, like text, images, logos etc here'''
        self.style = style
        self.camp = camp
        pygwrap.default_border.render( screen , self )
        if style == "difficulty":
            self.just_print_example(screen, self.x + 6, self.y + 25, "Current difficulty:", camp.get_difficulty(camp.xp_scale))

        '''if style == "s":
            # Display things for settings menu
            self.just_print_example(screen, self.x + 6, self.y+25, "Label example", "")
        '''

class ActualMenu (rpgmenu.Menu):
    ''' Class that is a child of rpgmenu, meaning you can add menu items to it. Is same size as overall menu Rect'''
    def __init__( self, screen, border=None, predraw=None, fontSize=14 ):
        x = screen.get_width() // 2 - (ViewDrawer.WIDTH / 2)
        y = screen.get_height() // 2 - ViewDrawer.HEIGHT // 2 + 40 + pygwrap.BIGFONT.get_linesize() * 2
        super(ActualMenu, self).__init__(screen,x,y,ViewDrawer.WIDTH,ViewDrawer.HEIGHT - pygwrap.BIGFONT.get_linesize() * 2, border=border, fontSize=fontSize)
        self.predraw = predraw

class ViewReDrawer( object ):
    ''' Class that redraws the view whenever it is updated, like the user changing active menu item. Adds a permanent caption section. view=the main ViewDrawer'''
    def __init__( self, border_rect=None, backdrop="bg_wests_stonewall5.png", menu=None, view=None, screen=None, caption=None, predraw=None, style= "s", camp=None ):
        self.backdrop = image.Image( backdrop )
        self.counter = 0
        self.view = view
        self.style = style
        self.camp = camp;

        if screen and not border_rect:
            border_rect = pygame.Rect( screen.get_width()//2 + 64, screen.get_height()//2 - ViewDrawer.HEIGHT//2 + 32, ViewDrawer.WIDTH - 64, ViewDrawer.HEIGHT )
        self.rect = border_rect

        # caption rectangle init
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
            self.view.render_permanent_stuff( screen, self.style, self.camp)

        # redraw caption rectangle
        if self.caption and self.caption_rect:
            pygwrap.default_border.render( screen , self.caption_rect )
            pygwrap.draw_text( screen, pygwrap.BIGFONT, self.caption, self.caption_rect, justify = 0 )
        self.counter += 4   # for spacing out backdrop tile
