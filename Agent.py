from enum import Enum
import copy
import numpy as np
from Percept import get_neighbors
from config import *

class Action(Enum):
    TURN_LEFT = 0 # Quay trái
    TURN_RIGHT = 1 # Quay phải
    TURN_DOWN = 2 # Quay sau
    MOVE_FORWARD = 3 # Đi thẳng
    GRAB = 4  # Thu vàng
    SHOOT = 5 # Bắn cung
    CLIMB = 6 # Leo ra khỏi hang động


def Identify_TurnType(agent_pos, agent_direction, new_pos):
    # Xác định hướng của new_pos so với agent_pos
    dx, dy = new_pos[0] - agent_pos[0], new_pos[1] - agent_pos[1]
    d = (dx, dy)
    if d == (1,0):
        new_direction = 'R'
    elif d == (0,1):
        new_direction = 'U'
    elif d == (-1,0):
        new_direction = 'L'
    else:
        new_direction = 'D'
    # Xác định TurnType(xoay trái, phải, sau hoặc không xoay)
    type_direction = np.array(['R','U','L','D'])
    old_index = np.where(type_direction == agent_direction)[0][0]
    new_index = np.where(type_direction == new_direction)[0][0]
    temp = new_index - old_index
    if temp == 0:
        return 'No'
    elif temp == 1:
        return Action.TURN_LEFT
    elif temp == -1:
        return Action.TURN_RIGHT
    else:
        return Action.TURN_DOWN
    
def Turn(agent_direct, type_turn):
    '''
        Hướng của Agent sau khi xoay.
    '''
    type_direction = np.array(['R','U','L','D'])
    index = np.where(type_direction == agent_direct)[0][0]
    # Xử lí hướng
    if type_turn == Action.TURN_RIGHT:
        index -= 1
    elif type_turn == Action.TURN_LEFT:
        index += 1
    elif type_turn == Action.TURN_DOWN:
        index += 2
    # Xử lí ngoại lệ
    if index == -1:
        index = 3
    if index >3:
        index = index - 4
    return type_direction[index]

def IsTurn(agent_pos, pos, agent_direction, path):
    '''
        Xem thử có cần điều hướng trước khi hành động không, nếu có thì điều hường
    '''
    TypeTurn = Identify_TurnType(agent_pos, agent_direction, pos)
    if TypeTurn != 'No':
        agent_direction = Turn(agent_direction, TypeTurn)
        path.append(TypeTurn)
    return agent_direction, path

def Move_Forward(agent_pos, agent_direction, cave, score):
    '''Di chuyển thẳng theo direction'''
    if agent_direction == 'R':
        dx, dy = (1,0)
    elif agent_direction == 'U':
        dx, dy = (0,1)
    elif agent_direction == 'L':
        dx, dy = (-1,0)
    elif agent_direction == 'D':
        dx, dy = (0,-1)
    # Vị trí mới của Agent
    x, y = agent_pos
    new_x, new_y = x + dx, y + dy
    agent_pos1 = map_pos(agent_pos)
    new_pos1 = map_pos((new_x,new_y))
    # Kiểm tra thử có khi di chuyển có va vào tường không
    state_bump = False
    if (new_x > 10 or new_x <1) or (new_y > 10 or new_y < 1):
        return agent_pos, cave, score, True
    else:
        new_pos = (new_x, new_y)
        # Cập nhật ô cũ
        cave1 = np.copy(cave)
        if cave1[agent_pos1[0],agent_pos1[1]] == 'A':
            cave1[agent_pos1[0],agent_pos1[1]] = '-'
        else:
            cave1[agent_pos1[0],agent_pos1[1]] = cave1[agent_pos1[0],agent_pos1[1]].replace('A','')
        # cập nhật lại ô mới
        if cave1[new_pos1[0],new_pos1[1]] == '-':
            cave1[new_pos1[0],new_pos1[1]] = 'A'
        else:
            cave1[new_pos1[0],new_pos1[1]] += 'A'
        # Cập nhật điểm
        score -= 10
        return new_pos, cave1, score, state_bump
        
def Shoot(KB, pos, cave, n, score):
    '''
    Bắn cung, có thể trúng Wumpus hoặc không :v
    '''
    pos1 = map_pos(pos)
    state = False 
    cave1 = copy.deepcopy(cave)
    delete_list = {}
    list_w = []
    list_stench = []
    if 'W' in cave1[pos1[0],pos1[1]]:
        state = True # Scream
        if cave1[pos1[0],pos1[1]] == 'W':
            cave1[pos1[0],pos1[1]] = '-'
            list_w.append((pos1[0],pos1[1]))
        else:
            cave1[pos1[0],pos1[1]] = cave1[pos1[0],pos1[1]].replace('W','')
            list_w.append((pos1[0],pos1[1]))

        list_stenchs = get_neighbors(pos,n)

        for stench in list_stenchs:
            del_stench_flag = True
            check_if_wumpus = get_neighbors(stench,n)
            for if_wumpus in check_if_wumpus:
                if_wumpus1 = map_pos(if_wumpus)
                if cave1[if_wumpus1[0],if_wumpus1[1]] == 'W':
                    del_stench_flag = False
                    break

            if del_stench_flag:
                # Cập nhật map
                    stench1 = map_pos(stench)   
                    list_stench.append((stench1[0],stench1[1]))
                    if cave1[stench1[0],stench1[1]] == 'S':
                        cave1[stench1[0],stench1[1]] = '-'
                    else:
                        cave1[stench1[0],stench1[1]] = cave1[stench1[0],stench1[1]].replace('S','')
                    # Cập nhật KB
                    literal_stench = int('1' + str(stench[0]) + str(stench[1]))
                    del_exist_stench = [literal_stench]
                    KB.del_clause(del_exist_stench)
                    add_loss_stench = [- literal_stench]
                    KB.add_clause(add_loss_stench)
                    delete_clauses = [clause for clause in KB.KB if (len(clause) >= 2 and (literal_stench in clause or 
                                                                                            -literal_stench in clause))]
                    for clause in delete_clauses:
                        if clause in KB.KB:
                            KB.del_clause(clause)

    delete_list['wumpus_pos'] = list_w
    delete_list['stench_pos'] = list_stench
    # Cập nhật score
    score -= 100
    return cave1, score, state, delete_list
                    
def Grab(agent_pos, cave, score):
    agent_pos1 = map_pos(agent_pos)
    x,y = agent_pos1
    # Cập nhật cave
    cave1 = np.copy(cave)
    if cave1[x,y] == 'G':
        cave1[x,y] == '-'
    else:
        cave1[x,y] = cave1[x,y].replace('G','')
    # Cập nhật điểm
    score += 100
    return cave1, score

def Climb(score):
    score += 10
    return score