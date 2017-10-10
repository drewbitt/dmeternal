import re
from characters import *

# Regular expression to help pyconsole.Console recognize a custom function called through the developer console
re_function = re.compile(r'(?P<name>\S+)(?P<params>[\(].*[\)])')

# Runs command input if the input matches the conditions of reg-ex re_function. Matches the input to a function defined for the dev console.
def console_func(console, match):
	func = console.convert_token(match.group("name"))
	params = console.convert_token(match.group("params"))
	
	if not isinstance(params, tuple):
		params = [params]
	try:
		out = func(*params)
	except Exception, strerror:
		console.output(strerror)
	else:
		console.output(out)

def reset_pc_health(party):
    '''\
		Restore the health of all party members
		Arguments:
		   party -- a reference to the party of the current campaign
			 |- reset_health(party) - Example of how to call command
	'''
    for pc in party:
        pc.hp_damage = 0

def reset_pc_mana(party):
    '''\
		Restore the mana of all party members
		Arguments:
		   party -- a reference to the party of the current campaign
			 |- reset_mana(party) - Example of how to call command
	'''
    for pc in party:
        pc.mp_damage = 0

def super_stats_trigger(party):
    '''\
		Modifies the stats of all player characters to be equal to 99
		Arguments:
		   party -- a reference to the party of the current campaign
			 |- super_stats(party) - Example of how to call command
	'''
    for pc in party:
        for stat in stats.PRIMARY_STATS:
            pc.statline[ stat ] = 99