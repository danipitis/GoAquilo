# models.py
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import pygame
import random

import constants
import settings

class Terrorist(pygame.sprite.Sprite):
	""" Terrorist class loads the enemy image and handles the moving on the y axes"""
	def __init__(self, filename):

		pygame.sprite.Sprite.__init__(self)

		# Load the image
		self.image = filename.convert()

		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()

	def reset_pos(self):
		self.rect.y = random.randrange(-200, -20)
		self.rect.x = random.randrange(constants.SCREEN_WIDTH -20)

	def update(self):

		# Move the enemy down with the speed of the current level
		self.rect.y += settings.current_level
       
class Player(pygame.sprite.Sprite):
	""" This class loads the player image and handles the moving on the x axes"""
	def __init__(self, filename):

		pygame.sprite.Sprite.__init__(self) 

		# Convert the image took from resources
		self.image = filename.convert()

		self.rect = self.image.get_rect()

		#Start the player from the middle-bottom screen
		self.rect.x = self.x_coord = constants.SCREEN_WIDTH // 2
		self.rect.y = self.y_coord = constants.SCREEN_HEIGHT - 58
		# 58 is the height of the player image

		# Speed in pixels per frame
		self.x_speed = 0


	def update(self):

		self.rect.x = self.x_coord

	def change_speed(self):
		check_x_border = self.x_coord + self.x_speed

		if check_x_border > 0 and check_x_border < 775:
			self.x_coord += self.x_speed


class Bullet(pygame.sprite.Sprite):
	""" This class represents the bullet """
	def __init__(self):

		pygame.sprite.Sprite.__init__(self) 

		self.image = pygame.Surface([4, 10])
		self.image.fill(constants.BLACK)

		self.rect = self.image.get_rect()

	def update(self):
		""" Move the bullet by 10 pixels """
		self.rect.y -= 10