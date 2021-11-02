import pygame
import sys
import os

# define your variables
board = (640, 640)
grid = (16, 16)
tile = (board[0] / grid[0], board[1] / grid[1])
black = pygame.Color(0, 0, 0)
white = pygame.Color("white")
# draw your board in a function


def draw_board():
    s.fill(black)
    for x in range(grid[0]):
        for y in range(grid[1]):
            if (x + y) % 2 == 0:
                cell = (x * tile[0], y * tile[1], tile[0], tile[1])
                pygame.draw.rect(s, white, cell)


pygame.init()
s = pygame.display.set_mode(board)
draw_board()
pygame.display.flip()
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
