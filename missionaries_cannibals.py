import sys
import pygame

"""
Game "Missionaries and Cannibals"
goal bring everyone safely to the opposite bank
Author: Maciej Dębiec
Date: 13-12-2020
"""

WIN_SIZE = (640, 480)
IMAGE_SCALE = (50, 50)
IMG_RAFT_SCALE = (3*IMAGE_SCALE[0], 2*IMAGE_SCALE[1])
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GAMEGRAPH = {
            "3-3-1": {"m": "2-3-0", "c": "3-2-0", "mm": "1-3-0",
                      "cc": "3-1-0", "mc": "2-2-0"},
            "3-2-0": {"c": "3-3-1"},
            "3-1-0": {"c": "3-2-1", "mm": "3-3-1"},
            "2-2-0": {"m": "3-2-1", "c": "2-3-1", "mc": "3-3-1"},
            "3-2-1": {"m": "2-2-0", "c": "3-1-0", "mm": "1-2-0",
                      "cc": "3-0-0", "mc": "2-1-0"},
            "3-0-0": {"c": "3-1-1", "cc": "3-2-1"},
            "3-1-1": {"m": "2-1-0", "c": "3-0-0", "mm": "1-1-0",
                      "mc": "2-0-0"},
            "1-1-0": {"m": "2-1-1", "c": "1-2-1", "mm": "3-1-1",
                      "cc": "1-3-1", "mc": "2-2-1"},
            "2-2-1": {"m": "1-2-0", "c": "2-1-0", "mm": "0-2-0",
                      "cc": "2-0-1", "mc": "1-1-0"},
            "0-2-0": {"m": "1-2-1", "c": "0-3-1", "mm": "2-2-1",
                      "mc": "1-3-1"},
            "0-3-1": {"c": "0-2-0", "cc": "0-1-0"},
            "0-1-0": {"m": "1-1-1", "c": "0-2-1", "mm": "2-1-1",
                      "cc": "0-3-1", "mc": "1-2-1"},
            "1-1-1": {"m": "0-1-0", "c": "1-0-0", "mc": "0-0-0"},
            "0-2-1": {"c": "0-1-0", "cc": "0-0-0"},

            "2-3-0": "failure",
            "1-3-0": "failure",
            "2-3-1": "failure",
            "1-2-0": "failure",
            "2-1-0": "failure",
            "2-0-0": "failure",
            "2-1-1": "failure",
            "1-2-1": "failure",
            "1-3-1": "failure",
            "2-0-1": "failure",
            "1-0-0": "failure",
            "0-0-0": "success"}


def getmouse():
    """returns mouse position if mouse is clicked"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            return mouse_position


def isready_ferry(mouse_position, passengers):
    """
    user is choosing characters to be brought to the opposite bank
    returns true if user clicked on raft and raft has 1-2 characters
    """
    if len(passengers) <= 2:
        for actor in passengers:
            if actor["rect"].collidepoint(mouse_position):
                if actor not in actors_left:
                    actors_left.append(actor)
                    actors_right.remove(actor)
                passengers.remove(actor)
                actors_left_display()
    if len(passengers) < 2:
        for actor in actors_left:
            if actor["rect"].collidepoint(mouse_position):
                passengers.append(actor)
                if len(passengers) == 2:
                    actor["rect"].left = passengers[0]["rect"].right
                else:
                    actor["rect"].left = raft_rect.left
                    + (passengers[0]["rect"].right - raft_rect.left)
                actor["rect"].bottom = raft_rect.top
    if raft_rect.collidepoint(mouse_position) and len(passengers) > 0:
        if len(passengers) == 2:
            passengers[1]["rect"].left = passengers[0]["rect"].right
        return True
    return False


def ferry(who, step):
    """ moving raft, chosen characters to opposite bank"""
    done = False
    raft_rect.left = who[0]["rect"].left
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))
        if raft_rect.right > arena.right - IMAGE_SCALE[1]:
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def isready_comeback(mouse_position, passengers):
    """
    user is choosing characters to be brought back
    returns true if user clicked on raft and raft has 1-2 characters
    """
    if len(passengers) <= 2:
        for actor in passengers:
            if actor["rect"].collidepoint(mouse_position):
                if actor not in actors_right:
                    actors_left.remove(actor)
                    actors_right.append(actor)
                    actors_right_display()
                passengers.remove(actor)
    if len(passengers) < 2:
        for actor in actors_right:
            if actor["rect"].collidepoint(mouse_position):
                passengers.append(actor)
                if len(passengers) == 2:
                    actor["rect"].left = passengers[0]["rect"].right
                else:
                    actor["rect"].left = raft_rect.left
                actor["rect"].bottom = raft_rect.top
    if raft_rect.collidepoint(mouse_position) and len(passengers) > 0:
        return True
    return False


def comeback(who, step):
    """ moving raft, chosen characters to left side"""
    done = False
    raft_rect.right = who[len(who)-1]["rect"].right
    for actor in who:
        actor["rect"] = actor["rect"].move((-step, 0))
        if raft_rect.left < arena.left + IMAGE_SCALE[1]:
            actor["rect"] = actor["rect"].move((step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def get_state_key(passengers):
    """
    returns key which is used in graf,
    depending on amaunt of characters on raft and their kind
    """
    count_cannibal = 0
    count_missionar = 0
    for actor in passengers:
        if actor in cannibals:
            count_cannibal += 1
        if actor in missionaries:
            count_missionar += 1
    if count_missionar == 1 and count_cannibal == 0:
        return "m"
    if count_missionar == 1 and count_cannibal == 1:
        return "mc"
    if count_missionar == 2 and count_cannibal == 0:
        return "mm"
    if count_cannibal == 2 and count_missionar == 0:
        return "cc"
    if count_cannibal == 1 and count_missionar == 0:
        return "c"


def weclome():
    """ displaying welcome screen """
    msg_distance = 10
    weclome_font = pygame.font.Font("freesansbold.ttf", 38)
    control_font = pygame.font.Font('freesansbold.ttf', 18)
    warning_font = pygame.font.Font('freesansbold.ttf', 18)
    goal_font = pygame.font.Font("freesansbold.ttf", 15)

    msg_welcome = weclome_font.render("Welcome", True, WHITE)
    msg_welcome_box = msg_welcome.get_rect()
    msg_welcome_box.center = arena.center

    msg_controls = control_font.render("Mouse control", True, WHITE)
    msg_controls_box = msg_controls.get_rect()
    msg_controls_box.top = msg_welcome_box.bottom + msg_distance
    msg_controls_box.left = msg_welcome_box.left + msg_distance

    msg_warning = warning_font.render(
        "Do not leave missionaries outnumberedby cannibals on the same bank",
        True,
        RED
         )
    msg_warning_box = msg_warning.get_rect()
    msg_warning_box.top = msg_controls_box.bottom + msg_distance
    msg_warning_box.left = arena.left + msg_distance

    msg_goal = goal_font.render(
        "Bring everyone safely to the opposite bank,"
        + " 1-2 characters can be on raft",
        True,
        WHITE
        )
    msg_goal_box = msg_goal.get_rect()
    msg_goal_box.left = arena.left + msg_distance
    msg_goal_box.top = msg_warning_box.bottom + msg_distance

    window.blit(msg_welcome, msg_welcome_box)
    window.blit(msg_controls, msg_controls_box)
    window.blit(msg_warning, msg_warning_box)
    window.blit(msg_goal, msg_goal_box)
    pygame.display.flip()
    pygame.time.wait(3000)


def failure():
    """ displaying failure screen"""
    failure_font = pygame.font.Font('freesansbold.ttf', 48)
    msg_failure = failure_font.render("Failure", True, RED)
    msg_failure_box = msg_failure.get_rect()
    msg_failure_box.center = arena.center
    window.blit(msg_failure, msg_failure_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def success():
    """ displaying success screen"""
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Success", True, WHITE)
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def game_display(counter):
    """ displays score"""
    score_font = pygame.font.Font("freesansbold.ttf", 18)
    msg_score = score_font.render(f"Score : {counter}", True, WHITE)
    msg_score_box = msg_score.get_rect()
    msg_score_box.bottom = arena.bottom
    msg_score_box.left = arena.right/2
    window.fill(pygame.Color("green"))
    window.blit(raft, raft_rect)
    window.blit(msg_score, msg_score_box)
    for actor in actors_right:
        window.blit(actor["surf"], actor["rect"])
    for actor in actors_left:
        window.blit(actor["surf"], actor["rect"])

    pygame.display.flip()
    fpsClock.tick(120)


def actors_right_display():
    """
    set position of actors on right bank
    that there is no gap between characters
    """
    for i, actor in enumerate(actors_right):
        actor["rect"].midright = (
            arena.right,
            (actors_right.index(actor)+1)*arena.height/7
            )


def actors_left_display():
    """
    set position of actors on left bank
    that there is no gap between characters
    """
    for i, actor in enumerate(actors_left):
        actor["rect"].midleft = (
            0,
            (i+1)*arena.height/7
            )


pygame.init()
fpsClock = pygame.time.Clock()
window = pygame.display.set_mode(WIN_SIZE)
arena = window.get_rect()

cannibal_1 = {"file": "cannibal.png"}
cannibal_2 = {"file": "cannibal.png"}
cannibal_3 = {"file": "cannibal.png"}
missionar_1 = {"file": "missionar.png"}
missionar_2 = {"file": "missionar.png"}
missionar_3 = {"file": "missionar.png"}

img_raft = pygame.image.load("raft.png")
raft = pygame.transform.scale(img_raft, IMG_RAFT_SCALE)
raft_rect = raft.get_rect()
raft_rect.left = IMAGE_SCALE[1]
raft_rect.top = arena.bottom/2

actors_left = [
    cannibal_1,
    cannibal_2,
    cannibal_3,
    missionar_1,
    missionar_2,
    missionar_3
]

actors_right = []

cannibals = [
    cannibal_1,
    cannibal_2,
    cannibal_3
]

missionaries = [
    missionar_1,
    missionar_2,
    missionar_3
]
for i, actor in enumerate(actors_left):
    image = pygame.image.load(actor["file"])
    actor["surf"] = pygame.transform.scale(image, IMAGE_SCALE)
    actor["rect"] = actor["surf"].get_rect()
    actor["rect"].midleft = (0, (i+1)*arena.height/7)


def main():
    counter = 0
    ferry_step = 5
    action = "listen"
    gamestate = "3-3-1"
    passengers = []
    weclome()
    while True:
        if action == "listen":
            mouse_position = getmouse()
            if mouse_position is not None:
                if isready_ferry(mouse_position, passengers):
                    action = "ferry"
        if action == "ferry":
            done = ferry(passengers, ferry_step)
            if done:
                counter += 1
                state_key = get_state_key(passengers)
                gamestate = GAMEGRAPH[gamestate][state_key]
                if GAMEGRAPH[gamestate] == "failure":
                    action = "failure"
                elif GAMEGRAPH[gamestate] == "success":
                    action = "success"
                else:
                    action = "unload"
        if action == "unload":
            mouse_position = getmouse()
            if mouse_position is not None:
                if isready_comeback(mouse_position, passengers):
                    action = "comeback"
        if action == "comeback":
            done_comeback = comeback(passengers, ferry_step)
            if done_comeback:
                state_key = get_state_key(passengers)
                gamestate = GAMEGRAPH[gamestate][state_key]
                passengers[0]["rect"].left = raft_rect.left
                counter += 1
                if GAMEGRAPH[gamestate] == "failure":
                    action = "failure"
                elif GAMEGRAPH[gamestate] == "success":
                    action = "success"
                else:
                    action = "listen"
        if action == "failure":
            failure()
            sys.exit()
        if action == "success":
            success()
            sys.exit()

        game_display(counter)


if __name__ == "__main__":
    main()
