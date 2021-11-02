import pygame
import random
import math
import sys

black = (0, 0, 0)
white = (255, 255, 255)
pygame.init()
scr = pygame.display.set_mode((360, 240))
win = scr.get_rect()
box = pygame.Rect(0, 0, 30, 30)
box.center = win.center
vec = [2, 1]
fps = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    box = box.move(vec)
    if box.left < win.left or box.right > win.right:
        vec[0] = -vec[0]
    if box.top < win.top or box.bottom > win.bottom:
        vec[1] = -vec[1]
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.display.flip()

    fps.tick(60)
