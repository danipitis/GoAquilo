# load_images.py Version 1.0.0
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan@gmail.com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import pygame
import constants

class LoadImages(object):
    """ LoadImages class handles the images from the game"""
    image            = None
    background_image = None

    # Load a specific image from the file path
    def get_image(self, file_name, colorkey = None):
        try:
            if colorkey is not None:
                self.image = pygame.image.load(constants.RESOURCE_PATH + file_name)
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            self.image.set_colorkey(colorkey, pygame.RLEACCEL)
            return self.image

        except pygame.error, message:
            self._print_error(file_name)
            raise SystemExit, message

    # Load the background image
    def get_background(self, file_name):
        try:
            background_image = pygame.image.load(constants.RESOURCE_PATH + file_name).convert()
            return background_image

        except pygame.error, message:
            self._print_error(file_name)
            raise SystemExit, message

    def _print_error(self, file_name):
        err = 'Unable to load image:', file_name
        print err8