# game.py
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import pygame
import random

import constants
import models
import timer
import load_images
import settings

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

	solider_shooting 	  = images_handler.get_image("solider_shooting.png", constants.WHITE)
	solider_not_shooting  = images_handler.get_image("solider_not_shooting.png", constants.WHITE)
	terrorist             = images_handler.get_image("terrorist.png", constants.WHITE)

	def __init__(self):
		self.score     = 0
		self.game_over = False

		self.all_sprites_list = pygame.sprite.Group()
		self.bullet_list      = pygame.sprite.Group()
		self.block_list       = pygame.sprite.Group()

		settings.reset()

		# Load the background image
		self.background_image      = self.images_handler.get_background("background.png")

		# Create the enemies
		self._add_enemies(settings.spawned_enemies)

		# Create the player
		self._add_player()

	def process_events(self):
		# Game logic below
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.MOUSEBUTTONDOWN:
				self._shoot_event()

			# User pressed down on a key
			# Default speed is 4 px
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.x_speed = - constants.PLAYER_SPEED
				if event.key == pygame.K_RIGHT:
					self.player.x_speed = constants.PLAYER_SPEED
				if event.key == pygame.K_RETURN:
					if self.game_over:
						self.__init__()
				if event.key == pygame.K_SPACE:
					self._shoot_event()

			# User let up a key
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					if self.player.x_speed != constants.PLAYER_SPEED:
					 self.player.x_speed = 0
				if event.key == pygame.K_RIGHT:
					if self.player.x_speed != - constants.PLAYER_SPEED:
					 self.player.x_speed = 0

		return False

	def _shoot_event(self):
		# Shoot a bullet
		self._shoot_bullet()

		# Change is_shooting state			
		self.is_shooting = True
		self.shoot_timer.start()			


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
				self.player.rect.y = constants.SCREEN_HEIGHT - 57
				# 57 is the height of the not_shooting_image
			else:
				self.player.image = self.solider_shooting.convert()
				self.player.rect.y = constants.SCREEN_HEIGHT - 78	
				# 78 is the height of the shooting_image

			# print("x= ", x_coord, "y= ", y_coord)

			# Display what we have drawn
			self.all_sprites_list.update()

			# Calculate mechanics for each bullet
			self._bullet_mechanics()

			self._update_level()

			self._check_game_over()

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

		# Prints scores (current lifes, enemies killed and level)
		self._print_scores(screen)

		pygame.display.flip()

	def _bullet_mechanics(self):
		for bullet in self.bullet_list:
 
 			# Check is bullet hit an enemy
			block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)

			# For each block hit, remove the bullet and increment the score
			for block in block_hit_list:
				self.bullet_list.remove(bullet)
				self.all_sprites_list.remove(bullet)
				self.score += 1

			# Remove the bullet if passes the screen
			if bullet.rect.y < -10:
				self.bullet_list.remove(bullet)
				self.all_sprites_list.remove(bullet)

	def _print_text(self, screen, message, size, x_axes, y_axes):
		font = pygame.font.SysFont(None, size)
		text = font.render(message, True, constants.BLACK)
		x_axes -= text.get_width() // 2
		y_axes -= text.get_height() // 2
		screen.blit(text, [x_axes, y_axes])

	def _print_game_over(self, screen):

			center_x = (constants.SCREEN_WIDTH // 2)
			center_y = (constants.SCREEN_HEIGHT // 2)
			self._print_text(screen,"Game over!", 25, center_x, center_y)

			center_y += 50
			self._print_text(screen,"PRESS ENTER to start again", 25, center_x, center_y)
	
	def _print_scores(self, screen):
		# Update kills text
		text_x_axes  = constants.SCREEN_WIDTH / 2
		text_y_axes  = 25
		text_message = "Kills: %s" % self.score
		self._print_text(screen, text_message, 35, text_x_axes, text_y_axes)

		text_x_axes  = 50
		text_message = "Lifes: %s" % settings.current_lifes
		self._print_text(screen, text_message, 35, text_x_axes, text_y_axes)

		text_x_axes  = constants.SCREEN_WIDTH - 75
		text_message = "Level: %s" % settings.current_level
		self._print_text(screen, text_message, 35, text_x_axes, text_y_axes) 

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

		# Set the bullet so it is where the player gun is, thats why i added + 10
		bullet.rect.x = self.player.rect.x + 10
		bullet.rect.y = self.player.rect.y - 24

		# Add the bullet to the lists
		self.all_sprites_list.add(bullet)
		self.bullet_list.add(bullet)

	def _check_game_over(self):
		if settings.current_lifes == 0:
			self.game_over = True

		for enemy in self.block_list:

			if enemy.rect.y > constants.SCREEN_HEIGHT:
				settings.current_lifes -= 1
				self.block_list.remove(enemy)
				# print "Current life ", settings.current_lifes

			if pygame.sprite.collide_rect(self.player, enemy) == True:
				self.game_over = True

	def _update_level(self):
		if len(self.block_list) == 0:
			settings.current_level += 1
			# print "Current level", settings.current_level
			self._add_enemies(settings.spawned_enemies)

	def _delete_end_bullets(self):
		for bullet in self.bullet_list:
			self.all_sprites_list.remove(bullet)