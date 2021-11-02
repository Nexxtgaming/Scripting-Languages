import pygame
import random
import math
import sys

win = (800, 800)
white = pygame.Color("white")
pygame.init()
s = pygame.display.set_mode(win)
s.fill(white)
list_circles = []
for i in range(10000):
    is_in_window = False
    rgb = random.randint(0, 0xFFFFFFFF)
    color = pygame.color.Color(rgb)
    radius = random.randint(10, 50)
    center = (random.randint(0, win[0]), random.randint(0, win[1]))
    width = 0
    collision = False
    circle = (center, radius)
    if center[0] - radius > 0 and center[0] + radius < win[0]:
        if center[1] - radius > 0 and center[1] + radius < win[1]:
            is_in_window = True
    for x0, y0, r0 in list_circles:
        d = math.sqrt((center[0] - x0) ** 2 + (center[1] - y0) ** 2)
        if d < radius + r0:
            collision = True
            break
    if is_in_window is True and not collision:
        pygame.draw.circle(s, color, center, radius, width)
        pygame.display.flip()
        list_circles.append((center[0], center[1], radius))
while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN):
            pygame.quit()
            sys.exit()
