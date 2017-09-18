
import util
from bigmenu import ViewDrawer
import pygwrap
import pygame

class DevMenu( pygame.Rect ):

    def __init__( self, screen, border=pygwrap.default_border, predraw=None, fontSize=14 ):

        x = screen.get_width() // 2 - (ViewDrawer.WIDTH / 2)
        y = screen.get_height() // 2 - ViewDrawer.HEIGHT // 2 + 40 + pygwrap.BIGFONT.get_linesize() * 2
        w= ViewDrawer.WIDTH
        h = ViewDrawer.HEIGHT - pygwrap.BIGFONT.get_linesize() * 2

        super(DevMenu, self).__init__(x,y,w,h)

        self.screen = screen
        self.border = border
        self.MENUFONT = pygame.font.Font( util.image_dir( "VeraBd.ttf" ) , fontSize)
        self.predraw = predraw

    def render(self, do_extras=True):
        if do_extras:
            if self.predraw:
                self.predraw( self.screen )
            if self.border:
                self.border.render( self.screen , self )

        # do some rendering of dev console stuff here

    def wait_for_input(self):
        no_exit = True

        while no_exit:
            pc_input = pygwrap.wait_event()

            if pc_input.type == pygwrap.TIMEREVENT:
                # Redraw the menu on each timer event.
                self.render()
                pygame.display.flip()

            # Deal with mouse stuff here? needed if need to click on dev console.
            # probably true if we need to click on input section of dev console, but can
            # just always have this active. or may need if want to copy output

            # may need to check to see if we are actively in focus with the text-enter box,
            # if we ever allow it to not be in focus

            elif pc_input.type == pygame.KEYDOWN:
                if pc_input.key == pygame.K_UP:
                    # recall last command? here
                    no_exit = False
                elif pc_input.key == pygame.K_RETURN:
                    # execute dev console command here
                    no_exit = False
                elif pc_input.unicode == u"`":
                    # just exit menu
                    no_exit = False

                # may need to add mouse button up/down events here

                elif pc_input.type == pygame.QUIT:
                    no_exit = False
