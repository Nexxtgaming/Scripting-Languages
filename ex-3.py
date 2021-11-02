import pygame
import sys

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
pygame.init()
scr = pygame.display.set_mode((360, 240))
win = scr.get_rect()
box1 = pygame.Rect(0, 0, 30, 30)
box1.center = win.center
box2 = pygame.Rect(0, 0, 30, 60)
box2.midleft = win.midleft
vec = [1, 0]
pygame.key.set_repeat(50, 50)
fps = pygame.time.Clock()
step = 5
myfont = pygame.font.Font("freesansbold.ttf", 48)
msg = myfont.render("The Game !!!", True, red)
msg_box = msg.get_rect()
msg_box.center = win.center
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                box2 = box2.move(0, -step)
            if event.key == pygame.K_DOWN:
                box2 = box2.move(0, step)
    box1 = box1.move(vec)
    if box1.left < win.left or box1.right > win.right:
        vec[0] = -vec[0]
    if (
        box1.left < box2.right
        and abs(box1.centery - box2.centery) < (box1.h + box2.h) / 2
    ):
        vec[0] = -vec[0]
    scr.fill(black)
    scr.blit(msg, msg_box)
    pygame.draw.rect(scr, white, box1)
    pygame.draw.rect(scr, white, box2)
    pygame.display.flip()
    fps.tick(260)
