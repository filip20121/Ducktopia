import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join

import sys
#local classes
sys.path.append('Classes/')
from Fire import Fire
from Block import Block
from Player import Player
WIDTH, HEIGHT = 1920, 800
FPS = 60
PLAYER_VEL = 5

pg.init()
pg.display.set_caption("Ducktopia")

window = pg.display.set_mode((0, 0), pg.FULLSCREEN)

def get_background(name):
    """
    Get the background image and tiles.

    :param name: Name of the background image
    
    :return: Tiles and the background image
    """
    image = pg.image.load(join("..\\assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    """
    Draw game elements on the window.

    :param window: Window to draw on
    :param background: Background tiles
    :param bg_image: Background image
    :param player: Player object
    :param objects: List of game objects
    :param offset_x: X-offset for scrolling
    """
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pg.display.update()


def handle_vertical_collision(player, objects, dy):
    """
    Handle vertical collision with game objects.

    :param player: Player object
    :param objects: List of game objects
    :param dy: Change in y-coordinate

    :return: List of collided objects
    """
    collided_objects = []
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    """
    Check collision with game objects.

    :param player: Player object
    :param objects: List of game objects
    :param dx: Change in x-coordinate

    :return: Collided object (if any)
    """
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    """
    Handle player movement.

    :param player: Player object
    :param objects: List of game objects
    """
    keys = pg.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pg.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pg.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def main(window):
    """
    Main loop of the game
    """
    # Initialize clock and background
    pg.display.init()
    clock = pg.time.Clock()
    background, bg_image = get_background("Gray.png")

    # Set up game elements
    block_size = 96
    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    offset_x = 200
    scroll_area_width = 0

    run = True
    while run:
        # Control frame rate
        clock.tick(FPS)
        
        for event in pg.event.get():
            # Handle quit event
            if event.type == pg.QUIT:
                run = False
                break

            # Handle keydown event
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player.jump_count < 2:
                    player.jump()

        # Update player and fire animation
        player.loop(FPS)
        fire.loop()

        # Handle player movement
        handle_move(player, objects)

        # Draw game elements on the window
        draw(window, background, bg_image, player, objects, offset_x)

        # Scroll the screen based on player's position
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

    # Quit the game
    pg.quit()
    quit()


if __name__ == "__main__":
    main(window)
