import sys
import pygame

pygame.init()
green = (0, 255, 0)
size = width, height = (320, 240)
speed = [2, -2]

screen = pygame.display.set_mode(size)
win = screen.get_rect()


img = pygame.image.load("spiral.png")
img_rect = img.get_rect()
img_rect.center = win.center

fpsClock = pygame.time.Clock()

# newimg = img

angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    newimg = pygame.transform.rotate(img, angle)
    #newimg = pygame.transform.rotate(newimg, angle)
    newimg_rect = newimg.get_rect()
    newimg_rect.center = img_rect.center

    angle = (angle + 20) % 360

    screen.fill(green)
    screen.blit(newimg, newimg_rect)
    pygame.display.flip()
    fpsClock.tick(30)
