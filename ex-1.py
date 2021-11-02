import pygame, sys, math

black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
scr = pygame.display.set_mode((800, 400))
win = scr.get_rect()
scr.fill(white)

left_center = (1/4*win.width, win.centery)
right_center = (3/4*win.width, win.centery)

line_length = 0.9*1/4*win.width

lines = 7

left_list = []
rigth_list = []

for i in range(lines):
    angle = (i/lines)*2*math.pi
    left_end = (left_center[0] + line_length*math.sin(angle),
                left_center[1] + line_length*math.cos(angle))

    right_end = (right_center[0] + line_length*math.sin(angle),
                 right_center[1] + line_length*math.cos(angle))

    left_list.append(left_end)
    rigth_list.append(right_end)

    pygame.draw.lines(scr, black, True, left_list, 10)

    pygame.draw.polygon(scr, black, rigth_list, 0)

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
