import os
import sys
import pygame
from pygame.locals import *

#start the game
pygame.init()

#consts
WIDTH = 1024
HEIGHT = 720
FPS = 60
CLOCK = pygame.time.Clock()

#display the window of size WIDTH x HEIGHT
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ducktopia")

#background image of window
background = pygame.image.load(os.path.join("Photos","background.png"))
#main loop
while (True):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            pass

        if event.type == KEYDOWN:
            pass

    display.blit(background,(0,0))

    pygame.display.update()
    CLOCK.tick(FPS)
