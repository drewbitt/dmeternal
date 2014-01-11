import base
from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell

COLORS = ( SOLAR, EARTH, WATER, FIRE, AIR, LUNAR )
COLOR_NAME = ( "Solar", "Earth", "Water", "Fire", "Air", "Lunar" )

import airspells
import lunarspells
import solarspells
import waterspells

# Compile the spells into a useful list.
SPELL_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if isinstance( o , Spell ):
            SPELL_LIST.append( o )

harvest( airspells )
harvest( lunarspells )
harvest( solarspells )
harvest( waterspells )


