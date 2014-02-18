# game.py Version 1.0.0
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan@gmail.com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import pygame
import random
import constants
import models
import timer
import load_images

class Game(object):
	""" Game class holding the methods for process events, game logic and objects display"""

	all_sprites_list = None
	bullet_list      = None
	block_list       = None

	game_over        = False
	is_shooting      = False
	done             = False
	score            = 0
	shoot_timer      = timer.Timer()


	images_handler = load_images.LoadImages()

	solider_shooting 	  = images_handler.get_image("solider_fire.png", constants.WHITE)
	solider_not_shooting  = images_handler.get_image("solider_not_shooting.png", constants.WHITE)
	terrorist             = images_handler.get_image("terrorist.png", constants.WHITE)

	def __init__(self):
		self.score     = 0
		self.game_over = False

		self.all_sprites_list = pygame.sprite.Group()
		self.bullet_list      = pygame.sprite.Group()
		self.block_list       = pygame.sprite.Group()

		# Load the background image
		self.background_image      = self.images_handler.get_background("background.png")

		# Create the enemies
		self._add_enemies(25)

		# Create the player
		self._add_player()

	def process_events(self):
		# Game logic below
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Shoot a bullet
				self._shoot_bullet()

				# Change is_shooting state			
				self.is_shooting = True
				self.shoot_timer.start()			

			# User pressed down on a key
			# Default speed is 4 px
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.x_speed = -4
				if event.key == pygame.K_RIGHT:
					self.player.x_speed = 4
				if event.key == pygame.K_RETURN:
					if self.game_over:
						self.__init__()

			# User let up a key
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					self.player.x_speed = 0
				if event.key == pygame.K_RIGHT:
					self.player.x_speed = 0

		return False


	def run_logic(self):

		if not self.game_over:
			self.player.change_speed()

			#For shooting state
			self.shoot_timer.end()

			if not self.shoot_timer.check_difference(40000):
				self.is_shooting = False

			# Graphics below

			if not self.is_shooting:
				self.player.image = self.solider_not_shooting.convert()
			else:
				self.player.image = self.solider_shooting.convert()

			# print("x= ", x_coord, "y= ", y_coord)

			# Display what we have drawn
			self.all_sprites_list.update()

			# Calculate mechanics for each bullet
			for bullet in self.bullet_list:
 
				# Check is bullet hit an enemy
				block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)

				# For each block hit, remove the bullet and add to the score
				for block in block_hit_list:
					self.bullet_list.remove(bullet)
					self.all_sprites_list.remove(bullet)
					self.score += 1

				# Remove the bullet if it flies up off the screen
				if bullet.rect.y < -10:
					self.bullet_list.remove(bullet)
					self.all_sprites_list.remove(bullet)

			if len(self.block_list) == 0:
				self.game_over = True

			for block in self.block_list:
				if block.rect.y > constants.SCREEN_HEIGHT:
					self.block_list.remove(block)
					#print "one down"


	def display_frame(self, screen):

		# Fill screen with the background image
		screen.blit(self.background_image, [0,0])


		self.all_sprites_list.draw(screen)

		if self.game_over:
			# Delete the remaining bullets when the game finishes
			self._delete_end_bullets()

			self._print_game_over(screen)
		else:
			self.all_sprites_list.draw(screen)

		font = pygame.font.SysFont(None, 35)
		text = font.render("You killed: %s" % self.score, True, constants.BLACK)
		textpos = text.get_rect(centerx=constants.SCREEN_WIDTH/2)
		textpos.top = 5
		screen.blit(text, textpos)

		pygame.display.flip()

	def _print_game_over(self, screen):
			font = pygame.font.SysFont(None, 25)
			first_line  = font.render("Game Over!", True, constants.BLACK)
			second_line = font.render("Press ENTER to start again", True, constants.BLACK)
			center_x = (constants.SCREEN_WIDTH // 2) - (first_line.get_width() // 2)
			center_y = (constants.SCREEN_HEIGHT // 2) - (first_line.get_height() // 2)
			screen.blit(first_line, [center_x, center_y])
			center_x = (constants.SCREEN_WIDTH // 2) - (second_line.get_width() // 2)
			center_y = (constants.SCREEN_HEIGHT // 2) - (second_line.get_height() // 2) + 50
			screen.blit(second_line, [center_x, center_y])	

	def _add_enemies(self, number_of_enemies):
		for i in range(number_of_enemies):
			# This represents a terrorist
			block = models.Terrorist(self.terrorist)

			# Set a random location for the block
			block.rect.x = random.randrange(constants.SCREEN_WIDTH  - 50)
			block.rect.y = random.randrange(constants.SCREEN_HEIGHT - 400)

			# Add the block to the list of objects
			self.block_list.add(block)
			self.all_sprites_list.add(block)

	def _add_player(self):
		self.player = models.Player(self.solider_not_shooting)
		self.all_sprites_list.add(self.player)

	def _shoot_bullet(self):
		# Fire a bullet if the user clicks the mouse button
		bullet = models.Bullet()

		# Set the bullet so it is where the player gun is, thats why i added + 14
		bullet.rect.x = self.player.rect.x + 14
		bullet.rect.y = self.player.rect.y

		# Add the bullet to the lists
		self.all_sprites_list.add(bullet)
		self.bullet_list.add(bullet)

	def _delete_end_bullets(self):
		for bullet in self.bullet_list:
			self.all_sprites_list.remove(bullet)
