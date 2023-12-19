import numpy as np
import pandas as pd

def read_map(path):
    with open('./Map/map1.txt') as f:
        n= int(f.readline().strip())
    df = pd.read_csv('./Map/map1.txt',skiprows=1,header=None)
    cave = np.vstack(df.apply(lambda x:x.values[0].split('.'),axis = 1).values)
    return cave

def map_pos(pos):
    x, y = pos
    new_x = 10 -y
    new_y = x - 1
    return (new_x, new_y)

agent_pos = (1,1)

n = 10