import sys
import math
import pygame

black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
scr = pygame.display.set_mode((800, 550))
scr.fill(white)
win = scr.get_rect()


def drawbranch(point1, point2, point3, point4, point5):
    pygame.draw.lines(scr, black, True, (point1, point2, point4, point5), 5)
    pygame.draw.lines(scr, black, True, (point2, point3, point4), 5)
    pygame.display.flip()


def drawgeometree(point1, point2, point3, point4, point5, n):
    drawbranch(point1, point2, point3, point4, point5)
    dx = point3[0] - point4[0]
    dy = point3[1] - point4[1]
    new_point2_right = [point3[0] - dx, point3[1] + dy]
    new_point4_right = [point4[0] - dx, point4[1] + dy]
    new_point3_right = [point4[0] - 2*dx, point4[1] + dy]
    new_point2_left = [point2[0] - dx, point2[1] - dy]
    new_point4_left = [point3[0] - dx, point3[1] - dy]
    new_point3_left = [point2[0] - dx, point2[1] - 2*dy]
    if n > 1:
        drawgeometree(point3, new_point2_right, new_point3_right, new_point4_right, point4, n - 1)
        drawgeometree(point2, new_point2_left, new_point3_left, new_point4_left, point3, n - 1)


def drawline(xa, ya, xb, yb, width):
    color = (255/width**4, 255/width, 255/width**4)
    s1, s2 = (win.centerx+xa, win.height-ya), (win.centerx+xb, win.height-yb)
    pygame.draw.line(scr, color, s1, s2, width)
    #pygame.display.flip()


def drawtree(x1, y1, x2, y2, n):
    drawline(x1, y1, x2, y2, n)

    # your code to compute x3,y3,x4,y4
    dx = (x2 - x1)*scale
    dy = (y2 - y1)*scale
    x3 = x2 + dx*cos1 - dy*sin1
    y3 = y2 + dx*sin1 + dy*cos1
    x4 = x2 + dx*cos2 - dy*sin2
    y4 = y2 + dx*sin2 + dy*cos2
    x5 = x2 + dx*cos3 - dy*sin3
    y5 = y2 + dx*sin3 + dy*cos3

    if n > 1:
        drawtree(x2, y2, x3, y3, n-1)
        drawtree(x2, y2, x4, y4, n-1)
        drawtree(x2, y2, x5, y5, n-1)

scale = 0.7
phi1 = math.radians(60)
phi2 = math.radians(-30)
phi3 = math.radians(10)
sin1 = math.sin(phi1); cos1 = math.cos(phi1)
sin2 = math.sin(phi2); cos2 = math.cos(phi2)
sin3 = math.sin(phi3); cos3 = math.cos(phi3)

#drawtree(0, 0, 0, 180, 8)
size = 100
start1 = [win[0], (win[1]/2) - (size/2)]
start2 = [win[0] - size, (win[1]/2) - (size/2)]
start3 = [win[0] - (size/2), win[1]/2]
start4 = [win[0] - size, (win[1]/2) + (size/2)]
start5 = [win[0], (win[1]/2) + size/2]
drawgeometree(start1, start2, start3, start4, start5, 10)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RETURN:
                sys.exit()
