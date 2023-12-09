import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join

class Object(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        """
        Initialize a game object.

        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param width: Width of the object
        :param height: Height of the object
        :param name: Name of the object
        """
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        """
        Draw the object on the window.

        :param win: Window to draw on
        :param offset_x: X-offset for scrolling
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

