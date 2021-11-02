import pygame
import sys
import math
from classes import *
import random
"""
Shooter game - player have to kill zombies spawning around him.
Author: Maciej Dębiec 234677
Date: 27.01.2021
"""
SIZE = (1100, 800)
GREEN = (150, 255, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SPAWNS_X = (60, SIZE[0]-60)
SPAWNS_Y = (SIZE[1]/2, SIZE[1]/3, 3*SIZE[1]/4)
WALLS_X = (100, SIZE[0]-100, 250, 400, 700, 800, 500, 800)
WALLS_Y = (SIZE[1]/2, SIZE[1]/2, SIZE[1]/2+50, 200, 200, 350, 600, 600)
WALLS_WIDTH = (30, 30, 30, 250, 200, 30, 200, 30)
WALLS_HEIGHT = (150, 100, 150, 30, 30, 150, 30, 150)
BACKGROUND_IMAGE = pygame.image.load("background_image.png")
pygame.init()
pygame.font.init()


def creating_map(wall_group):
    """create walls"""
    for i in range(8):
        wall = Wall(WALLS_X[i], WALLS_Y[i], WALLS_WIDTH[i], WALLS_HEIGHT[i])
        wall_group.add(wall)


def spawn_places(spawn_x, spawn_y):
    """ creates spawn places for zombies"""
    for x in range(40, SIZE[0], 40):
        spawn_x.append(x)
    for y in range(40, SIZE[1], 40):
        spawn_y.append(y)


def create_hp(wall_group, hp_group):
    """creates randomly health points"""
    space = 10
    rand_x = random.randint(space, SIZE[0] - space)
    rand_y = random.randint(space, SIZE[1] - space)
    new_hp = HealthPoint(rand_x, rand_y)
    walls = pygame.sprite.spritecollide(new_hp, wall_group, False)
    while len(walls) > 0:
        rand_x = random.randint(space, SIZE[0] - space)
        rand_y = random.randint(space, SIZE[1] - space)
        new_hp = HealthPoint(rand_x, rand_y)
        walls = pygame.sprite.spritecollide(new_hp, wall_group, True)
    hp_group.add(new_hp)


def spawning(zombie_group, wave_number, spawn_x, spawn_y):
    """spawns zombies randomly from both sides"""
    if wave_number < len(spawn_x):
        rand_x = random.sample(spawn_x, wave_number)
    else:
        rand_x = spawn_x
    if wave_number < len(spawn_y):
        rand_y = random.sample(spawn_y, wave_number)
    else:
        rand_y = spawn_y
    index_x = 0
    index_y_1 = 0
    index_y_2 = 0
    for i in range(wave_number):
        rand_side = random.randint(0, 1)
        if rand_side == 0:
            x_pos = SPAWNS_X[0]
            y_pos = rand_y[index_y_1]
            index_y_1 += 1
        if rand_side == 1:
            x_pos = SPAWNS_X[1]
            y_pos = rand_y[index_y_2]
            index_y_2 += 1
        if rand_side == 2:
            y_pos = 60
            x_pos = rand_x[index_x]
            index_x += 1
        new_zombie = Zombie(x_pos, y_pos)
        zombie_group.add(new_zombie)


def zombies_follow(player_group, player, zombie_group):
    """makes all zombies follow the player"""
    if player_group.has(player):
        for zombie in zombie_group:
            if not zombie.rect.colliderect(player.rect):
                zombie.follow(player)
            else:
                zombie.control(0, 0)
                zombie.kill_player(player)


def overcome_wall(zombie_group, wall_group):
    """makes zombies overcome walls"""
    tolerance = 10
    for zombie in zombie_group:
        walls = pygame.sprite.spritecollide(zombie, wall_group, False)
        if len(walls) > 0:
            for wall in walls:
                left_diff = abs(zombie.rect.right - wall.rect.left)
                bottom_diff = abs(zombie.rect.top - wall.rect.bottom)
                top_diff = abs(zombie.rect.bottom - wall.rect.top)
                rigth_diff = abs(zombie.rect.left - wall.rect.right)
                if left_diff < tolerance and bottom_diff < tolerance:
                    if zombie.vec_y < 0 and zombie.vec_x > 0:
                        if abs(zombie.vec_y) < abs(zombie.vec_x):
                            zombie.control(zombie.velocity, 0)
                        else:
                            zombie.control(0, -zombie.velocity)
                if left_diff < tolerance and top_diff < tolerance:
                    if zombie.vec_y > 0 and zombie.vec_x > 0:
                        if zombie.vec_y < zombie.vec_x:
                            zombie.control(zombie.velocity, 0)
                        else:
                            zombie.control(0, zombie.velocity)
                if rigth_diff < tolerance and top_diff < tolerance:
                    if zombie.vec_x < 0 and zombie.vec_y > 0:
                        if abs(zombie.vec_x) > abs(zombie.vec_y):
                            zombie.control(-zombie.velocity, 0)
                        else:
                            zombie.control(0, zombie.velocity)
                if rigth_diff < tolerance and bottom_diff < tolerance:
                    if zombie.vec_x < 0 and zombie.vec_y < 0:
                        if abs(zombie.vec_x) > abs(zombie.vec_y):
                            zombie.control(-zombie.velocity, 0)
                        else:
                            zombie.control(0, -zombie.velocity)
                if left_diff < tolerance:
                    if zombie.vec_x > 0:
                        zombie.control(0, zombie.velocity)
                if top_diff < tolerance:
                    if zombie.vec_y > 0:
                        if zombie.vec_x >= 0:
                            zombie.control(zombie.velocity, 0)
                        if zombie.vec_x < 0:
                            zombie.control(-zombie.velocity, 0)
                if rigth_diff < tolerance:
                    if zombie.vec_x < 0:
                        if zombie.vec_y >= 0:
                            zombie.control(0, zombie.velocity)
                        if zombie.vec_y < 0:
                            zombie.control(0, -zombie.velocity)
                if bottom_diff < tolerance:
                    if zombie.vec_y < 0:
                        zombie.control(0, zombie.velocity)


def collides_with_sprite(player, sprite_group, state):
    """checks if player collides with sprite from defined side"""
    tolerance = 15
    collided = pygame.sprite.spritecollide(player, sprite_group, False)
    if len(collided) == 0:
        return False
    for sprite in collided:
        if state == "top":
            difference = abs(sprite.rect.bottom - player.rect.top)
            if difference < tolerance:
                return True
        if state == "bottom":
            difference = abs(sprite.rect.top - player.rect.bottom)
            if difference < tolerance:
                return True
        if state == "left":
            difference = abs(sprite.rect.right - player.rect.left)
            if difference < tolerance:
                return True
        if state == "right":
            difference = abs(sprite.rect.left - player.rect.right)
            if difference < tolerance:
                return True
    return False


def key_event(player, zombie_group, wall_group):
    """handles key events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.rect.y > 0:
        col_zombie = collides_with_sprite(player, zombie_group, "top")
        col_wall = collides_with_sprite(player, wall_group, "top")
        if not col_zombie and not col_wall:
            player.control(0, -player.velocity)
        player.direction = "up"
    if keys[pygame.K_DOWN] and player.rect.y < SIZE[1]:
        col_zombie = collides_with_sprite(player, zombie_group, "bottom")
        col_wall = collides_with_sprite(player, wall_group, "bottom")
        if not col_zombie and not col_wall:
            player.control(0, player.velocity)
        player.direction = "down"
    if keys[pygame.K_LEFT] and player.rect.x > 0:
        col_zombie = collides_with_sprite(player, zombie_group, "left")
        col_wall = collides_with_sprite(player, wall_group, "left")
        if not col_zombie and not col_wall:
            player.control(-player.velocity, 0)
        player.direction = "left"
    if keys[pygame.K_RIGHT] and player.rect.x < SIZE[0]:
        col_zombie = collides_with_sprite(player, zombie_group, "right")
        col_wall = collides_with_sprite(player, wall_group, "right")
        if not col_zombie and not col_wall:
            player.control(player.velocity, 0)
        player.direction = "right"
    return keys


def is_clicked(button):
    """checks if user clicked the button"""
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button.collidepoint(pos):
                return True
    return False


def killing(zombie_group, bullet_group, wall_group):
    """
    makes bullet cannot pass walls
    then checks if there are any killed zombies
    returns amount of killed zombies
    """
    score = 0
    for wall in wall_group:
        pygame.sprite.spritecollide(wall, bullet_group, True)
    for bullet in bullet_group:
        dead = pygame.sprite.spritecollide(bullet, zombie_group, True)
        if len(dead) > 0:
            bullet.kill()
        score += len(dead)
    return score


def get_hp(player, points_group):
    """adds health if player collided with any health points"""
    taken_points = pygame.sprite.spritecollide(player, points_group, True)
    for point in taken_points:
        player.health += point.points


def health_handle(player, hp_group, screen):
    """handles player's health"""
    if player.health < 100:
        get_hp(player, hp_group)
    if player.health <= 0:
        dead_screen(screen, player.score)


def welcome_screen(screen):
    """
    displays controls for the game
    and play button
    """
    screen.fill(BLACK)
    font = pygame.font.Font("freesansbold.ttf", 20)
    button_font = pygame.font.Font("freesansbold.ttf", 35)
    score_font = pygame.font.Font("freesansbold.ttf", 25)
    mov_text = font.render("movement - w, a, s, d", True, RED)
    mov_rect = mov_text.get_rect()
    mov_rect.center = [SIZE[0]/2, SIZE[1]/2-100]
    fire_text = font.render("fire - space", True, RED)
    fire_rect = fire_text.get_rect()
    fire_rect.top = mov_rect.bottom
    fire_rect.left = mov_rect.left
    play = button_font.render("PLAY", True, RED)
    play_button = play.get_rect()
    play_button.top = fire_rect.bottom + 100
    play_button.left = fire_rect.left
    highscore = score_font.render(
        f"your highscore is: {get_highscore()}", True, RED
        )
    highscore_rect = highscore.get_rect()
    highscore_rect.center = (SIZE[0]/2, 200)
    screen.blit(mov_text, mov_rect)
    screen.blit(fire_text, fire_rect)
    screen.blit(play, play_button)
    screen.blit(highscore, highscore_rect)
    pygame.display.update()
    while not is_clicked(play_button):
        pygame.display.update()
    pygame.time.delay(500)


def display_background(screen, background):
    """ displays game background on screen"""
    screen.fill(WHITE)
    screen.blit(background, (0, 0))


def health_score_wave(screen, player, wave):
    """displays current health, score and wave number"""
    font = pygame.font.Font("freesansbold.ttf", 15)
    healt_text = font.render(
        f"health: {player.health} " +
        f" score: {player.score} wave {wave}", True, BLACK)
    healt_rect = healt_text.get_rect()
    healt_rect.center = (SIZE[0]/2, SIZE[1]-20)
    screen.blit(healt_text, healt_rect)


def draw_and_update(first_group, second_group, screen):
    """draws and updates two sprite groups"""
    first_group.update()
    second_group.update()
    first_group.draw(screen)
    second_group.draw(screen)


def draw_and_update_one(fist_group, screen):
    """ draws and update one sprite group on screen"""
    fist_group.update()
    fist_group.draw(screen)


def draw(first_group, second_group, screen):
    """ draws two sprite groups on screen"""
    first_group.draw(screen)
    second_group.draw(screen)


def dead_screen(screen, score):
    """displays screen with score after loosing the game"""
    dead_font = pygame.font.Font("freesansbold.ttf", 50)
    if int(get_highscore()) < score:
        set_highscore(score)
        dead_text = dead_font.render(
            "YOU ARE DEAD. " +
            f"New Highscore: {score} !!!", True, RED
            )
    else:
        dead_text = dead_font.render(
            f"YOU ARE DEAD. score: {score}", True, RED
            )
    dead_rect = dead_text.get_rect()
    dead_rect.center = (SIZE[0]/2, SIZE[1]/2)
    screen.fill(BLACK)
    screen.blit(dead_text, dead_rect)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


def get_highscore():
    """returns user's highscore from txt file"""
    with open("highscore.txt", "r") as file:
        highscore = file.read()
    return highscore


def set_highscore(highscore):
    """sets user's highscore to the txt file"""
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))


def main():
    screen = pygame.display.set_mode(SIZE)
    background = pygame.transform.scale(BACKGROUND_IMAGE, SIZE)

    clock = pygame.time.Clock()
    previous_shoot_time = pygame.time.get_ticks()
    previous_spawn_time = pygame.time.get_ticks()
    previous_hp_time = pygame.time.get_ticks()

    player = Player(SIZE[0]/2, SIZE[1]/2)
    zombie = Zombie(15, SIZE[1]/2)
    health_point = HealthPoint(300, 650)

    hp_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    zombie_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    player_group.add(player)
    zombie_group.add(zombie)
    hp_group.add(health_point)

    spawn_time = 2000
    wave = 1
    wave_changed = False
    time_changed = False
    spawn_x = []
    spawn_y = []
    welcome_screen(screen)
    creating_map(wall_group)
    spawn_places(spawn_x, spawn_y)
    while True:
        current_time = pygame.time.get_ticks()
        keys = key_event(player, zombie_group, wall_group)
        if keys[pygame.K_SPACE]:
            if current_time - previous_shoot_time > player.shoot_delay:
                if player_group.has(player):
                    bullet_group.add(player.create_bullet())
                    previous_shoot_time = pygame.time.get_ticks()

        spawn_time_diff = current_time - previous_spawn_time
        if len(zombie_group.sprites()) == 0 and spawn_time_diff > spawn_time:
            wave += 1
            wave_changed = True
        if wave_changed and not time_changed:
            previous_spawn_time = pygame.time.get_ticks()
            time_changed = True
        if spawn_time_diff > spawn_time and wave_changed:
            spawning(zombie_group, wave, spawn_x, spawn_y)
            time_changed = False
            wave_changed = False
        if current_time - previous_hp_time > health_point.spawn_time:
            create_hp(wall_group, hp_group)
            previous_hp_time = pygame.time.get_ticks()

        zombies_follow(player_group, player, zombie_group)
        overcome_wall(zombie_group, wall_group)
        display_background(screen, background)
        health_score_wave(screen, player, wave)
        draw(wall_group, hp_group, screen)
        draw_and_update(player_group, zombie_group, screen)
        draw_and_update_one(bullet_group, screen)
        player.score += killing(zombie_group, bullet_group, wall_group)
        health_handle(player, hp_group, screen)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
