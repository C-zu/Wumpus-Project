import pygame
import pandas as pd
import time
from Game import *
from KnowledgeBase import *
from Percept import *
from Room import *
from Agent import *
from config import *


pygame.init()
FONT = pygame.font.Font(None, 14)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus")



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


def create_map(cave,path_line):
    N = len(cave)
    for row in range(len(cave)):
        for col in range(len(cave)):
            pygame.draw.rect(screen, GRAY, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
def draw_objects(cave, path_line):
    N = len(cave)
    for row in range(len(cave)):
        for col in range(len(cave)):
            if cave[row, col] != "-" and (row, col) in path_line:
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
                if "P" in cave[row, col]:
                    screen.blit(pit, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                      get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
def print_footstep(foot_step,n):
    for i in foot_step:
        screen.blit(footstep, (get_map_pos_y(n, CELL_SIZE) + (i[1] + 0.25) * CELL_SIZE,
                get_map_pos_x(n, CELL_SIZE) + (i[0] + 0.25) * CELL_SIZE))

def main(maptext):
    screen.blit(BG, (0, 0))
    n, cave, agent_pos = read_map(maptext)
    KB, heuristic, path, list_agent_pos, cave1, list_score = Solve_Wumpus_World(agent_pos, 'R', n, cave)
    for i in range(len(path)):
        if type(path[i]) is tuple:
            path[i] = map_pos(path[i],n)
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
    path_line = []
    foot_step = []
    while (run):
        if (path_i < len(path)):
            create_map(cave,path_line)
            if type(path[path_i]) is tuple:
                current_path = path[path_i]
                path_line.append(path[path_i])
                foot_step = path_line.copy()
                while (len(foot_step) > 3):
                    foot_step.pop(0)
                for i in path_line:
                    pygame.draw.rect(screen, BROWN, (get_map_pos_y(n, CELL_SIZE) + i[1] * CELL_SIZE, get_map_pos_x(n, CELL_SIZE) + i[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                screen.blit(agent, (get_map_pos_y(n, CELL_SIZE) + (path[path_i][1]+0.25) * CELL_SIZE,
                                    get_map_pos_x(n, CELL_SIZE) + (path[path_i][0]+0.25) * CELL_SIZE))
                time.sleep(0.25)
            elif type(path[path_i]) is dict:
                time.sleep(0.25)
                for i in path_line:
                    pygame.draw.rect(screen, BROWN, (
                    get_map_pos_y(n, CELL_SIZE) + i[1] * CELL_SIZE, get_map_pos_x(n, CELL_SIZE) + i[0] * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE), 0)
                if path[path_i]['wumpus_pos']:
                    for i in path[path_i]['wumpus_pos']:
                        screen.blit(wumpus_die, (get_map_pos_y(n, CELL_SIZE) + i[1] * CELL_SIZE,
                                                 get_map_pos_x(n, CELL_SIZE) + i[0] * CELL_SIZE))
                        cave[i[0], i[1]] = cave[i[0], i[1]].replace("W", "")
                        time.sleep(0.3)
                if path[path_i]['stench_pos']:
                    for i in path[path_i]['stench_pos']:
                        cave[i[0], i[1]] = cave[i[0], i[1]].replace("S", "")


            elif type(path[path_i]) is not tuple:
                for i in path_line:
                    pygame.draw.rect(screen, BROWN, (
                    get_map_pos_y(n, CELL_SIZE) + i[1] * CELL_SIZE, get_map_pos_x(n, CELL_SIZE) + i[0] * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE), 0)
                if path[path_i].value in direction_changes:
                    agent_dir, agent = direction_changes[path[path_i].value][agent_dir]
                elif (path[path_i].value == 3):
                    agent = agent
                elif (path[path_i].value == 4):
                    cave[current_path[0], current_path[1]] = cave[current_path[0], current_path[1]].replace("G", "")
                elif (path[path_i].value == 5):
                    if agent_dir == "LEFT":
                        agent = agent_left_shoot
                    elif agent_dir == "RIGHT":
                        agent = agent_right_shoot
            print_footstep(foot_step[:-1],n)
            draw_objects(cave,  path_line)
            screen.blit(agent, (get_map_pos_y(n, CELL_SIZE) + (current_path[1]+0.25) * CELL_SIZE,
                                    get_map_pos_x(n, CELL_SIZE) + (current_path[0]+0.25) * CELL_SIZE))
            path_i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()