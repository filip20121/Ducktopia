from Object import Object
from Player import load_sprite_sheets
import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        """
        Initialize a fire trap object.

        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param width: Width of the fire trap
        :param height: Height of the fire trap
        """
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pg.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        """
        Turn on the fire trap.
        """
        self.animation_name = "on"

    def off(self):
        """
        Turn off the fire trap.
        """
        self.animation_name = "off"

    def loop(self):
        """
        Update the state of the fire trap in the game loop.
        """
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

