import pygame
import sys
import math

black, white = (0, 0, 0), (255, 255, 255)

pygame.init()
scr = pygame.display.set_mode((500, 500))
win = scr.get_rect()
scr.fill(white)


def drawline3d(a, b, w=1):    # a, b -> ap, bp
    xa, ya, za = a[0], a[1], a[2]
    xb, yb, zb = b[0], b[1], b[2]
    # convert 3d to 2d with cabinet projection
    xap = xa - za * sinphi * k
    yap = ya - za * cosphi * k
    xbp = xb - zb * sinphi * k
    ybp = yb - zb * cosphi * k
    # convert to screen coordinates and draw
    s1 = (win.centerx + xap, win.centery - yap)
    s2 = (win.centerx + xbp, win.centery - ybp)
    pygame.draw.line(scr, black, s1, s2, w)


def drawfigure3d(figure):
    even = figure[0::2]
    odd = figure[1::2]
    for a, b in zip(even, odd):  # read pairs of 3d-points
        drawline3d(a, b)


def rotx(fig, a):
    newfig = []
    sin, cos = math.sin(a), math.cos(a)
    for x, y, z in fig:
        newfig.append((x, y*cos-z*sin, y*sin+z*cos))
    return newfig


def roty(fig, a):
    newfig = []
    sin, cos = math.sin(a), math.cos(a)
    for x, y, z in fig:
        newfig.append((x*cos+z*sin, y, -x*sin+z*cos))
    return newfig


def rotz(fig, a):
    newfig = []
    sin, cos = math.sin(a), math.cos(a)
    for x, y, z in fig:
        newfig.append((x*cos-y*sin, x*sin+y*cos, z))
    return newfig


k = 0.5                     # projection scale
phi = math.radians(63.4)    # try also 45
sinphi, cosphi = math.sin(phi), math.cos(phi)

angle = math.radians(5)    # rotation angle

s = 100

# P0, P1, P2, P3 = (-s, -s, -s), (-s, s, -s), (s, s, -s), (s, -s, -s)
# P4, P5, P6, P7 = (-s, -s, s), (-s, s, s), (s, s, s), (s, -s, s)
P1 = (-s, s, -s)
P4, P5, P6 = (-s, -s, s), (-s, s, s), (s, s, s)
O1, = (0, s, 0)
cube = (P6, P1, P1, P4, P4, P5, P5, P6,
P4, P6, P5, P1)

pygame.key.set_repeat(50, 50)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RETURN:
                sys.exit()
            if event.key == pygame.K_x:
                cube = rotx(cube, angle)
            if event.key == pygame.K_y:
                cube = roty(cube, angle)
            if event.key == pygame.K_z:
                cube = rotz(cube, angle)

    scr.fill(white)
    drawfigure3d(cube)
    pygame.display.flip()