import numpy as np
import pandas as pd
import pygame

WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GRAY = (128,128,128)
BROWN = (218,165,32)

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
footstep = pygame.image.load("images/footstep.png")

wumpus = pygame.transform.scale(wumpus, (CELL_SIZE, CELL_SIZE))
wumpus_die = pygame.transform.scale(wumpus_die, (CELL_SIZE, CELL_SIZE))
agent_right = pygame.transform.scale(agent_right, (CELL_SIZE // 2, CELL_SIZE // 2))
agent_left = pygame.transform.scale(agent_left, (CELL_SIZE // 2, CELL_SIZE // 2))
agent_up = pygame.transform.scale(agent_up, (CELL_SIZE // 2, CELL_SIZE // 2))
agent_down = pygame.transform.scale(agent_down, (CELL_SIZE // 2, CELL_SIZE // 2))
agent_right_shoot = pygame.transform.scale(agent_right_shoot, (CELL_SIZE // 2, CELL_SIZE // 2))
agent_left_shoot = pygame.transform.scale(agent_left_shoot, (CELL_SIZE // 2, CELL_SIZE // 2))
footstep = pygame.transform.scale(footstep, (CELL_SIZE // 2, CELL_SIZE // 2))
breeze = pygame.transform.scale(breeze, (CELL_SIZE, CELL_SIZE))
stench = pygame.transform.scale(stench, (CELL_SIZE, CELL_SIZE))
gold = pygame.transform.scale(gold, (CELL_SIZE, CELL_SIZE))
pit = pygame.transform.scale(pit, (CELL_SIZE, CELL_SIZE))
door = pygame.transform.scale(door, (CELL_SIZE, CELL_SIZE))

BG = pygame.transform.scale(pygame.image.load("images/background.png"),(1280,720))

def get_font(size):
  return pygame.font.Font("font/font.ttf", size)

def get_map_pos_y(N, CELL_SIZE, WIDTH=WIDTH):
    return WIDTH // 2 - (CELL_SIZE * N // 2)


def get_map_pos_x(N, CELL_SIZE, HEIGHT=HEIGHT):
    return HEIGHT // 2 - (CELL_SIZE * N // 2)

def map_pos2(pos,n):
    '''
        Chuyển từ pos từ numpy ra theo yêu cầu, dùng để tìm vị trí ban đầu của
    '''
    x, y = pos
    new_x = y + 1
    new_y = n - x
    return (new_x, new_y)

def map_pos(pos,n):
    '''
        Chuyển từ pos theo yêu cầu của đề ra numpy
    '''
    x, y = pos
    new_x = n - y
    new_y = x - 1
    return (new_x, new_y)

def read_map(path):
    with open(path) as f:
        n= int(f.readline().strip())
    df = pd.read_csv(path,skiprows=1,header=None)
    cave = np.vstack(df.apply(lambda x:x.values[0].split('.'), axis = 1).values)
    # Lấy agent_pos
    pos_x = np.where(np.char.find(cave, 'A') != -1)[0][0]
    pos_y = np.where(np.char.find(cave, 'A') != -1)[1][0]
    agent_pos = map_pos2((pos_x, pos_y),n)
    return n, cave, agent_pos


