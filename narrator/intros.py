
from plots import Plot,PlotError
import context
import items
import maps
import mapgen
import waypoints
import monsters
import dialogue
import services
import teams
import characters

class LightOfTheMacguffin( Plot ):
    LABEL = "INTRO_1"
    propp = context.PROPP_INTERDICTION
    setting = context.SET_RENFAN
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the setting to be None or RenFan."""
        if pstate.setting in (None,context.SET_RENFAN):
            return True
    def custom_init( self, nart ):
        """Load *INTRO_2, create MACGUFFIN"""
        self.register_element( "MACGUFFIN", items.choose_item() )
        self.add_sub_plot( nart, "INTRO_2", ident="next" )
        return True

class OurMacguffinIsGone( Plot ):
    LABEL = "INTRO_2"
    scope = True
    @classmethod
    def matches( self, pstate ):
        """Requires the propp to be INTERDICTION, MACGUFFIN to exist."""
        return pstate.propp == context.PROPP_INTERDICTION and pstate.elements.get( "MACGUFFIN" )
    def custom_init( self, nart ):
        sp = self.add_sub_plot( nart, "CITY_SCENE" )
        if sp:
            nart.camp.scene = sp.elements.get( "SCENE" )
            nart.camp.entrance = sp.elements.get( "ENTRANCE" )
            return True

class CityOnEdgeOfCiv( Plot ):
    LABEL = "CITY_SCENE"
    def custom_init( self, nart ):
        """Create map, fill with city + services."""
        myscene = maps.Scene( 129, 129, sprites={maps.SPRITE_WALL: "terrain_wall_lightbrick.png"},
            biome=context.HAB_FOREST, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        mymapgen = mapgen.EdgeOfCivilization( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="SCENE" )

        castle = self.register_element( "CITY", mapgen.CastleRoom( width=35,height=35,tags=(context.CIVILIZED,), parent=myscene ) )
        myroom = mapgen.FuzzyRoom( tags=(context.ENTRANCE,), parent=castle )
        myteam = teams.Team( strength=0, default_reaction=characters.SAFELY_FRIENDLY)
        castle.contents.append( myteam )
        myent = waypoints.Waypoint()
        myroom.contents.append( myent )
        myroom.contents.append( monsters.generate_npc(team=myteam) )
        myroom.contents.append( monsters.generate_npc(team=myteam) )

        self.register_element( "ENTRANCE", myent )

        self.add_sub_plot( nart, "CITY_WEAPONSHOP" )
        self.add_sub_plot( nart, "CITY_LIBRARY" )
        self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "ENCOUNTER" )

        return True

class BasicEncounter( Plot ):
    LABEL = "ENCOUNTER"
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("SCENE")
    def custom_init( self, nart ):
        room = mapgen.FuzzyRoom()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.level, 
          habitat=self.elements.get("SCENE").get_encounter_request() ) )
        self.register_element( "_ROOM", room, dident="SCENE" )
        return True






