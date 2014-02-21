# aquilo.py Version 1.1.0
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import pygame
import os

from scripts import constants
from scripts import game

def main():
	# Game window goes on the center screen
	os.environ['SDL_VIDEO_CENTERED'] = '1'

	# Let the fun begin        
	pygame.init()

	size   = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("GoAquilo")
	# Uncomment the next line to hide the mouse arrow
	# pygame.mouse.set_visible(False)

	done  = False
	clock = pygame.time.Clock()

	game_instance = game.Game()

	# While the game has not ended
	while not done:

		done = game_instance.process_events()

		# Update object positions, check for collisions
		game_instance.run_logic()

		# Draw the current frame
		game_instance.display_frame(screen)	

		# Set frames per second
		clock.tick(constants.FPS)

pygame.quit()

if __name__ == "__main__":
	main()