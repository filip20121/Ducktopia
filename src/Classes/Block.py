from Object import Object
import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join


def get_block(size):
    """
    Get a block for terrain.

    :param size: Size of a block.

    :return: Block of terrain.
    """
    path = join("..\\assets", "Terrain", "Terrain.png")
    image = pg.image.load(path).convert_alpha()
    surface = pg.Surface((size, size), pg.SRCALPHA, 32)
    rect = pg.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pg.transform.scale2x(surface)


class Block(Object):
    def __init__(self, x, y, size):
        """
        Initialize a block object.

        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param size: Size of the block
        """
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pg.mask.from_surface(self.image)

