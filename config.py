import numpy as np
import pandas as pd

def map_pos(pos):
    '''
        Chuyển từ pos theo yêu cầu của đề ra numpy
    '''
    x, y = pos
    new_x = 10 - y
    new_y = x - 1
    return (new_x, new_y)

def map_pos2(pos):
    '''
        Chuyển từ pos từ numpy ra theo yêu cầu, dùng để tìm vị trí ban đầu của
    '''
    x, y = pos
    new_x = y + 1
    new_y = 10 - x
    return (new_x, new_y)
def read_map(path):
    with open(path) as f:
        n= int(f.readline().strip())
    df = pd.read_csv(path,skiprows=1,header=None)
    cave = np.vstack(df.apply(lambda x:x.values[0].split('.'),axis = 1).values)
    # Lấy agent_pos
    pos_x = np.where(cave == 'A')[0][0]
    pos_y = np.where(cave == 'A')[1][0]
    agent_pos = map_pos2((pos_x, pos_y))
    return n, cave, agent_pos

n = 10