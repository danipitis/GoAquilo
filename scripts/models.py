# models.py Version 1.0.0
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan@gmail.com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import pygame
import constants
    
class Terrorist(pygame.sprite.Sprite):
	""" Terrorist class loads the enemy image and handles the moving on the y axes"""
	def __init__(self, filename):

		pygame.sprite.Sprite.__init__(self)

		# Load the image
		self.image = filename.convert()

		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()

	def update(self):

		# Move the enemy down one pixel
		self.rect.y += 1

# This class represents the player       
class Player(pygame.sprite.Sprite):
	""" This class loads the player image and handles the moving on the x axes"""
	def __init__(self, filename):

		pygame.sprite.Sprite.__init__(self) 

		# Convert the image took from resources
		self.image = filename.convert()

		self.rect = self.image.get_rect()

		#Start the player from the middle-bottom screen
		self.rect.x = self.x_coord = constants.SCREEN_WIDTH // 2
		self.rect.y = self.y_coord = constants.SCREEN_HEIGHT - 78
		# 80 is the height of the player image - 2 px so he is not "floating"

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
		""" Move the bullet by 5 pixels """
		self.rect.y -= 5