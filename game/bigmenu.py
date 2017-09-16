
# from charsheet import CharacterSheet
import rpgmenu
import pygwrap
import image
import pygame

class ViewDrawer ( pygame.Rect ):
    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.
    WIDTH = 320
    HEIGHT = 450
    BODY_Y = 70

    def __init__( self, x=0, y=0, screen = None ):
        if screen:
            x = screen.get_width() // 2 - self.WIDTH
            y = screen.get_height() // 2 - self.HEIGHT // 2 + 32
        super(ViewDrawer, self).__init__(x,y,self.WIDTH,self.HEIGHT)

        mybmp = pygame.Surface( (54,54))
        mybmp.fill((0,0,255))
        self.render(mybmp)

    def just_print( self, screen, x, y, text1, text2, width=120, color=pygwrap.TEXT_COLOR ):
        """Do proper justification for stat line at x,y."""
        if text1:
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, text1, pygame.Rect( x, y, width, 20 ), justify = -1, color=color )
        if text2:
            pygwrap.draw_text( screen, pygwrap.SMALLFONT, text2, pygame.Rect( x, y, width, 20 ), justify = 1, color=color )

    def render( self, screen ):
        pygwrap.default_border.render( screen , self )
        self.just_print(screen, self.x + 6, self.y+10, "EYY", "")

class ActualMenu (rpgmenu.Menu):
    def __init__( self, screen, predraw = None, border=None ):
        x = screen.get_width() // 2 - ViewDrawer.WIDTH
        y = screen.get_height() // 2 - ViewDrawer.HEIGHT // 2 + 40 + pygwrap.BIGFONT.get_linesize() * 2
        super(ActualMenu, self).__init__(screen,x,y,ViewDrawer.WIDTH,ViewDrawer.HEIGHT - pygwrap.BIGFONT.get_linesize() * 2, border=border)
        self.predraw = predraw

class ViewReDrawer( object ):

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
            self.view.render( screen )

        if self.caption and self.caption_rect:
            pygwrap.default_border.render( screen , self.caption_rect )
            pygwrap.draw_text( screen, pygwrap.BIGFONT, self.caption, self.caption_rect, justify = 0 )
        self.counter += 4
