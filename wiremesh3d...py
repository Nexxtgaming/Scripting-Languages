import pygame
import sys
import math

black, white = (0, 0, 0), (255, 255, 255)
pygame.init()

scr = pygame.display.set_mode((700, 700))
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


def z(scr_x, scr_y):
    x = (float(scr_x) / (scr_xlim)) * xlim
    y = (float(scr_y) / (scr_ylim)) * ylim

    #z = math.exp(-((x)**2 + (y)**2))

    z = math.exp(-((x)**2 + (y)**2*math.cos(x))) * math.sin(x)

    #d = math.sqrt((3.0*x)**2 + (3.0*y)**2)
    #if d==0: return scr_zlim
    #z = math.sin(d)/d*math.cos(d)

    return (z / zlim) * scr_zlim

# cabinet projection
k = 0.5
phi = math.radians(63.4)
sinphi, cosphi = math.sin(phi), math.cos(phi)

# rotation angle
angle = math.radians(5)

# drawing limits for screen - around (0,0,0)
scr_xlim, scr_ylim, scr_zlim = 150, 150, 150
scr_mesh = 5

# drawing limits for 3d space - around (0,0,0)
xlim, ylim, zlim = math.pi, math.pi, 1.0

# make wire-mesh

wiremesh = []
for x in range(-scr_xlim, scr_xlim, scr_mesh):
    for y in range(-scr_ylim, scr_ylim, scr_mesh):
        wiremesh.extend([(x, y, z(x, y)), (x+scr_mesh, y, z(x+scr_mesh, y))])
        wiremesh.extend([(x, y, z(x, y)), (x, y+scr_mesh, z(x, y+scr_mesh))])

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
                wiremesh = rotx(wiremesh, angle)
            if event.key == pygame.K_y:
                wiremesh = roty(wiremesh, angle)
            if event.key == pygame.K_z:
                wiremesh = rotz(wiremesh, angle)

    scr.fill(white)
    drawfigure3d(wiremesh)
    pygame.display.flip()