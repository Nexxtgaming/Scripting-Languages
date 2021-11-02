import sys
import pygame

pygame.init()
green = (0, 255, 0)
size = width, height = (320, 240)
speed = [1, 1]

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
# ball = ball.convert(ball)
ballrect = ball.get_rect()

fpsClock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, "screen.png")
            pygame.quit()
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(green)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    fpsClock.tick(120)
