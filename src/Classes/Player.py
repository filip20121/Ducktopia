import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join

def flip(sprites):
    """
    Flip sprites horizontally.

    :param sprites: Sprites of the character.

    :return: Flipped sprites.
    """
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Load sprite sheets.

    :param dir1: Location of...
    :param dir2: Location of...
    :param width: Width of a sprite in px.
    :param height: Height of a sprite in px.
    :param direction: Direction.

    :return: All sprites.
    """
    path = join("..\\assets", dir1, dir2)
    print(path)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pg.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

'''
class Player describe the main character
'''
class Player(pg.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3
    SPRITES = 0
    
    def __init__(self, x, y, width, height):
        """
        Initialize the main character.

        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param width: Width of the character.
        :param height: Height of the character.
        """
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    
        
    def jump(self):
        """
        Make the character jump.
        """
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        """
        Move the character.

        :param dx: Value to move the character in OX.
        :param dy: Value to move the character in OY.
        """
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        """
        Make the character hit.
        """
        self.hit = True

    def move_left(self, vel):
        """
        Move the character to the left.

        :param vel: Velocity.
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        """
        Move the character to the right.

        :param vel: Velocity.
        """
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        """
        Loop function for character movement.

        :param fps: Frames per second.
        """
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        """
        Handle character landing.
        """
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        """
        Handle character hitting head.
        """
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        """
        Update the character sprite.
        """
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        """
        Update the character.
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        """
        Draw the character on the window.

        :param win: Window to draw on.
        :param offset_x: X-coordinate offset.
        """
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

