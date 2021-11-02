import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
"""
It is a ping-pong game with two players.
Author : Maciej Dębiec
Date : 21.11.2020
"""


def is_point(ball, win, players_score):
    """
    Check if some player scored the point
    and add point to this player and also
    set ball's position to center of the window
    """
    if ball.right == win.right:
        pygame.time.delay(1000)
        players_score[0] += 1
        ball.center = win.center
        return True
    if ball.left == win.left:
        pygame.time.delay(1000)
        players_score[1] += 1
        ball.center = win.center
        return True
    return False


def restart_players(player1, player2, win):
    """
    reset players' position
    """
    player1.midleft = win.midleft
    player2.midright = win.midright


def player1_inside(player1, score_box, win):
    """
    player 1 stays inside the window
    """
    if player1.top < (win.top + score_box.bottom):
        player1.top = win.top + score_box.bottom
    if player1.bottom > win.bottom:
        player1.bottom = win.bottom


def player2_inside(player2, score_box, win):
    """
    player 2 stays inside the window
    """
    if player2.top < (win.top + score_box.bottom):
        player2.top = win.top + score_box.bottom
    if player2.bottom > win.bottom:
        player2.bottom = win.bottom


def main():
    pygame.init()
    pygame.display.set_caption("Ping Pong Game")
    scr = pygame.display.set_mode((500, 300))
    win = scr.get_rect()
    fps = pygame.time.Clock()
    ball = pygame.Rect(0, 0, 20, 20)
    ball.center = win.center
    player1 = pygame.Rect(0, 0, 15, 60)
    player1.midleft = win.midleft
    player2 = pygame.Rect(0, 0, 15, 60)
    player2.midright = win.midright
    players_score = [0, 0]
    score_font = pygame.font.Font("freesansbold.ttf", 15)
    score_table = score_font.render(f"Score: {players_score[0]}", True, WHITE)
    score_box = score_table.get_rect()
    score_box.top = win.top
    step = 5
    vec = [1, 1]
    pygame.key.set_repeat(20, 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2 = player2.move(0, -step)
                if event.key == pygame.K_DOWN:
                    player2 = player2.move(0, step)
                if event.key == pygame.K_w:
                    player1 = player1.move(0, -step)
                if event.key == pygame.K_s:
                    player1 = player1.move(0, step)

        ball = ball.move(vec)
        if ball.top < (win.top + score_box.bottom) or ball.bottom > win.bottom:
            vec[1] = -vec[1]
        if ball.colliderect(player1) or ball.colliderect(player2):
            vec[0] = -vec[0]

        player1_inside(player1, score_box, win)
        player2_inside(player2, score_box, win)

        if is_point(ball, win, players_score):
            restart_players(player1, player2, win)
        score_table = score_font.render(
            "Score: " + f"{players_score[0]}" +
            f" : {players_score[1]}", True, WHITE
        )

        scr.fill(BLACK)
        scr.blit(score_table, score_box)
        pygame.draw.rect(scr, WHITE, ball)
        pygame.draw.rect(scr, WHITE, player1)
        pygame.draw.rect(scr, WHITE, player2)
        pygame.display.flip()
        fps.tick(250)


if __name__ == "__main__":
    main()
