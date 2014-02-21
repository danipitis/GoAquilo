# settings.py
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import constants

current_level   = 1
current_lifes   = constants.CURRENT_LIFES 
spawned_enemies = constants.SPAWNED_ENEMIES

def reset():
	global current_level
	global current_lifes
	global spawned_enemies

	current_level   = 1
	current_lifes   = constants.CURRENT_LIFES
	spawned_enemies = constants.SPAWNED_ENEMIES 