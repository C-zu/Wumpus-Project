import pygame
import pandas as pd
import time
from Game import *
from KnowledgeBase import *
from Percept import *
from Room import *
from Agent import *

pygame.init()
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 14)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus")

wumpus = pygame.image.load("images/wumpus.png")
wumpus_die = pygame.image.load("images/wumpus_die.png")
agent_right = pygame.image.load("images/agent_right.png")
agent_left = pygame.image.load("images/agent_left.png")
agent_up = pygame.image.load("images/agent_up.png")
agent_down = pygame.image.load("images/agent_down.png")
agent_right_shoot = pygame.image.load("images/agent_right_shoot.png")
agent_left_shoot = pygame.image.load("images/agent_left_shoot.png")
breeze = pygame.image.load("images/breeze.png")
stench = pygame.image.load("images/stench.png")
gold = pygame.image.load("images/gold.png")
pit = pygame.image.load("images/pit.png")
door = pygame.image.load("images/door.png")

wumpus = pygame.transform.scale(wumpus, (CELL_SIZE, CELL_SIZE))
wumpus_die = pygame.transform.scale(wumpus_die, (CELL_SIZE, CELL_SIZE))
agent_right = pygame.transform.scale(agent_right, (CELL_SIZE, CELL_SIZE))
agent_left = pygame.transform.scale(agent_left, (CELL_SIZE, CELL_SIZE))
agent_up = pygame.transform.scale(agent_up, (CELL_SIZE, CELL_SIZE))
agent_down = pygame.transform.scale(agent_down, (CELL_SIZE, CELL_SIZE))
agent_right_shoot = pygame.transform.scale(agent_right_shoot, (CELL_SIZE, CELL_SIZE))
agent_left_shoot = pygame.transform.scale(agent_left_shoot, (CELL_SIZE, CELL_SIZE))
breeze = pygame.transform.scale(breeze, (CELL_SIZE, CELL_SIZE))
stench = pygame.transform.scale(stench, (CELL_SIZE, CELL_SIZE))
gold = pygame.transform.scale(gold, (CELL_SIZE, CELL_SIZE))
pit = pygame.transform.scale(pit, (CELL_SIZE, CELL_SIZE))
door = pygame.transform.scale(door, (CELL_SIZE, CELL_SIZE))


def get_map_pos_y(N, CELL_SIZE):
    return WIDTH // 2 - (CELL_SIZE * N // 2)


def get_map_pos_x(N, CELL_SIZE):
    return HEIGHT // 2 - (CELL_SIZE * N // 2)


def get_neighbors(pos, n):
    '''
    Kiểm tra những ô xung quanh
    '''
    neighbors = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x, y = pos[0] + dx, pos[1] + dy
        if (1 <= x < n and 1 <= y < n):
            neighbors.append((x, y))
    return neighbors


def create_map(cave):
    N = len(cave)
    for row in range(len(cave)):
        for col in range(len(cave)):
            if (cave[row, col] != "-"):
                if "B" in cave[row, col]:
                    screen.blit(breeze, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "W" in cave[row, col]:
                    screen.blit(wumpus, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "S" in cave[row, col]:
                    screen.blit(stench, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "G" in cave[row, col]:
                    screen.blit(gold, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                       get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "D" in cave[row, col]:
                    screen.blit(door, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                       get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "P" in cave[row, col]:
                    screen.blit(pit, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                      get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def main():
    n, cave, agent_pos = read_map('map/map1.txt')
    print(agent_pos)
    KB, heuristic, path, list_agent_pos, cave1, score = Solve_Wumpus_World((1, 1), 'R', 10, cave)
    print(score)
    print(heuristic)
    for i in range(len(path)):
        if type(path[i]) is tuple:
            path[i] = map_pos(path[i])
    print(path)
    direction_changes = {
        0: {"RIGHT": ("UP", agent_up), "LEFT": ("DOWN", agent_down), "UP": ("LEFT", agent_left),
            "DOWN": ("RIGHT", agent_right)},
        1: {"RIGHT": ("DOWN", agent_down), "LEFT": ("UP", agent_up), "UP": ("RIGHT", agent_right),
            "DOWN": ("LEFT", agent_left)},
        2: {"RIGHT": ("LEFT", agent_left), "LEFT": ("RIGHT", agent_right), "UP": ("DOWN", agent_down),
            "DOWN": ("UP", agent_up)}
    }
    run = True
    agent = agent_right
    agent_dir = "RIGHT"
    path_i = 0
    while (run):
        if (path_i < len(path)):
            screen.fill(WHITE)
            create_map(cave)
            if type(path[path_i]) is tuple:
                current_path = path[path_i]
                screen.blit(agent, (get_map_pos_y(10, CELL_SIZE) + path[path_i][1] * CELL_SIZE,
                                    get_map_pos_x(10, CELL_SIZE) + path[path_i][0] * CELL_SIZE))
                time.sleep(0.1)
            elif type(path[path_i]) is dict:
                time.sleep(0.2)
                if path[path_i]['wumpus_pos']:
                    for i in path[path_i]['wumpus_pos']:
                        screen.blit(wumpus_die, (get_map_pos_y(10, CELL_SIZE) + i[1] * CELL_SIZE,
                                                 get_map_pos_x(10, CELL_SIZE) + i[0] * CELL_SIZE))
                        cave[i[0], i[1]] = cave[i[0], i[1]].replace("W", "")
                        time.sleep(0.6)
                if path[path_i]['stench_pos']:
                    for i in path[path_i]['stench_pos']:
                        cave[i[0], i[1]] = cave[i[0], i[1]].replace("S", "")


            elif type(path[path_i]) is not tuple:
                if path[path_i].value in direction_changes:
                    agent_dir, agent = direction_changes[path[path_i].value][agent_dir]
                elif (path[path_i].value == 3):
                    agent = agent
                elif (path[path_i].value == 4):
                    cave[current_path[0], current_path[1]] = cave[current_path[0], current_path[1]].replace("G", "")
                elif (path[path_i].value == 5):
                    if agent_dir == "LEFT":
                        agent = agent_left_shoot
                    else:
                        agent = agent_right_shoot
            screen.blit(agent, (get_map_pos_y(10, CELL_SIZE) + current_path[1] * CELL_SIZE,
                                    get_map_pos_x(10, CELL_SIZE) + current_path[0] * CELL_SIZE))
            path_i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()
