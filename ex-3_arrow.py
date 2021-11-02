import sys, pygame, math

pygame.init()
green = (0, 255, 0)
speed = [1, -1]

screen = pygame.display.set_mode((320, 240))
win = screen.get_rect()

#img = pygame.image.load("arrow.png")
img = pygame.image.load("spzoid.png")
img_rect = img.get_rect()

tick = 0

fpsClock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, "screen.bmp")
            pygame.quit()
            sys.exit()

    img_rect = img_rect.move(speed)
    if img_rect.left < 0 or img_rect.right > win.width:
        img = pygame.transform.flip(img, True, False)
        speed[0] = -speed[0]
        
    if img_rect.top < 0 or img_rect.bottom > win.height:
        img = pygame.transform.flip(img, False, True)
        speed[1] = -speed[1]
        
    if tick % 20 == 0:
        tick = 0
        angle = 90*math.copysign(1.0, speed[0]*speed[1])
        img = pygame.transform.flip(img, True, False)
        img = pygame.transform.rotate(img, angle)
    tick += 1

    screen.fill(green)
    screen.blit(img, img_rect)
    pygame.display.flip()
    fpsClock.tick(180)

