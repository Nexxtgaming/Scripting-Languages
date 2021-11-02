import pygame
import math
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_IMAGE = pygame.image.load("player_top.png")
PLAYER_RIGHT = pygame.image.load("player_right.png")
PLAYER_BOTTOM = pygame.image.load("player_bottom.png")
PLAYER_LEFT = pygame.image.load("player_left.png")
ZOMBIE_RIGHT = pygame.image.load("zombie.png")
ZOMBIE_LEFT = pygame.image.load("zombie_left.png")
WALL_IMAGE = pygame.image.load("wall.png")
pygame.font.init()


class Player(pygame.sprite.Sprite):
    velocity = 2
    health = 100
    shoot_delay = 500
    direction = "right"
    score = 0
    gun_distance = 12
    right_hand = [0, gun_distance]

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def control(self, x, y):
        """moves the player"""
        self.x += x
        self.y += y

    def update(self):
        if self.direction == "right":
            self.image = PLAYER_RIGHT
            self.rect = self.image.get_rect()
            self.right_hand = [0, self.gun_distance]
        if self.direction == "up":
            self.image = PLAYER_IMAGE
            self.rect = self.image.get_rect()
            self.right_hand = [self.gun_distance, 0]
        if self.direction == "down":
            self.image = PLAYER_BOTTOM
            self.rect = self.image.get_rect()
            self.right_hand = [-self.gun_distance, 0]
        if self.direction == "left":
            self.image = PLAYER_LEFT
            self.rect = self.image.get_rect()
            self.right_hand = [0, -self.gun_distance]
        self.rect.center = [self.x, self.y]
        if self.health <= 0:
            self.kill()

    def create_bullet(self):
        """creates bullet"""
        bullet_x = self.x + self.right_hand[0]
        bullet_y = self.y + self.right_hand[1]
        return Bullet(bullet_x, bullet_y, self.direction)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([8, 3])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.direction = direction

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        if self.direction == "left":
            self.rect.x -= self.speed
        if self.direction == "up":
            new_image = pygame.transform.scale(self.image, (3, 8))
            self.image = new_image
            self.rect.y -= self.speed
        if self.direction == "down":
            new_image = pygame.transform.scale(self.image, (3, 8))
            self.image = new_image
            self.rect.y += self.speed
        if self.rect.x >= 1100 or self.rect.y >= 800:
            self.kill()


class Zombie(pygame.sprite.Sprite):
    damage = 10
    damage_delay = 400
    velocity = 1
    vec_x = 0
    vec_y = 0

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("zombie.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.last_attack = pygame.time.get_ticks()

    def control(self, x, y):
        """set the value of movement vectors"""
        self.vec_x = x
        self.vec_y = y

    def update(self):
        if self.vec_x < 0:
            self.image = ZOMBIE_LEFT
            self.rect = self.image.get_rect()
        if self.vec_x > 0:
            self.image = ZOMBIE_RIGHT
            self.rect = self.image.get_rect()
        if self.x < 1100:
            self.x += self.vec_x
        if self.y < 800:
            self.y += self.vec_y
        self.rect.center = [self.x, self.y]

    def follow(self, player):
        """makes the zombie follow the player"""
        d_x = player.rect.x - self.rect.x
        d_y = player.rect.y - self.rect.y
        vec_x = self.velocity/math.sqrt(2)
        vec_y = self.velocity/math.sqrt(2)
        if d_x == 0:
            vec_x = 0
        elif d_y == 0:
            vec_y = 0
        else:
            if d_x < 0:
                vec_x = -self.velocity/math.sqrt(1+math.pow(d_y/d_x, 2))
            else:
                vec_x = self.velocity/math.sqrt(1+math.pow(d_y/d_x, 2))
            vec_y = abs(vec_x) * (d_y/abs(d_x))
        self.control(vec_x, vec_y)

    def kill_player(self, player):
        """do damage to the player"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > self.damage_delay:
            player.health -= self.damage
            self.last_attack = pygame.time.get_ticks()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.color = (255, 255, 255)
        self.image = pygame.transform.scale(WALL_IMAGE, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class HealthPoint(pygame.sprite.Sprite):
    width = 20
    height = 10
    points = 10
    spawn_time = 45000
    font = pygame.font.Font("freesansbold.ttf", 20)

    def __init__(self, x, y):
        super().__init__()
        self.image = self.font.render(f"{self.points} HP", True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
