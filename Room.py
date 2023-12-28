from config import *
from Percept import *
import copy


def Info_Room(pos, cave,n):
    '''
        Info room tại vị trí của agent đang đứng.
    '''
    pos = map_pos(pos,n) # Chuyển đổi Pos để phù hợp với Numpy
    x,y  = pos 
    # Gán giá trị
    info_room = {'Stench': 0, 'Breeze':0, 'Gold': 0, 'Pit': 0, 'Wumpus': 0}
    if 'S' in cave[x, y]:
        info_room['Stench'] = 1
    if 'B' in cave[x,y]:
        info_room['Breeze'] = 1
    if 'G' in cave[x, y]:
        info_room['Gold'] = 1
    if 'P' in cave[x,y]:
        info_room['Pit'] = 1
    if 'W' in cave[x,y]:
        info_room['Wumpus'] = 1
    return info_room


def Literals_Room(info_room, pos):
    x, y = pos
    info_map = {'Stench': '1', 'Breeze': '2','Pit': '4', 'Wumpus': '5'}
    list_literals = []
    for name, value in info_map.items():
        if info_room[name] == 1:
            literal = [int(value + str(x) + str(y))]
        else:
            literal = [- int(value + str(x) + str(y))]
        list_literals.append(literal)
    return list_literals


def existStench(agent_pos, cave, n):
    info_room = Info_Room(agent_pos, cave, n)
    return info_room['Stench'] == 1
def existBreeze( agent_pos, cave, n):
    info_room = Info_Room(agent_pos, cave, n)
    return info_room['Breeze'] == 1
def existGold( agent_pos, cave, n):
    info_room = Info_Room(agent_pos, cave, n)
    return info_room['Gold'] == 1
def NoSB( agent_pos, cave, n):
    info_room = Info_Room(agent_pos, cave, n)
    return (info_room['Stench'] == 0 and info_room['Breeze'] == 0)

def is_filter(KB_temp,CNF):
    for literal in CNF:
        if [-literal] not in KB_temp:
            return False
    return True

def filter_KB(KB):
    for CNF in KB.KB:
        if len(CNF) > 1 and is_filter(KB.KB,CNF):
            KB.del_clause(CNF)
    return KB

def Identify_Safe_Rooms( KB, agent_pos, cave, n):
    info_room = Info_Room(agent_pos, cave,n)
    list_CNF = [Literals_Room(info_room, agent_pos)[2:]]
    if NoSB(agent_pos, cave,n):
        list_CNF.append(Not_SB_Case(agent_pos, n))
    if existStench(agent_pos, cave,n):
        list_CNF.append(Stench_Case(agent_pos, n))
    if existBreeze(agent_pos, cave,n):
        list_CNF.append(Breeze_Case(agent_pos, n))
    for CNF_i in list_CNF:
        for clause in CNF_i:
            KB.add_clause(clause)
    KB = filter_KB(KB)
    # Xác định các ô an toàn để đi
    safe_rooms = []
    wumpus_rooms = []
    pit_rooms = []
    neighbors, out_of_caves = get_neighbors(agent_pos, n)
    for neighbor in neighbors:
        clause1 = int(str(4) + str(neighbor[0]) + str(neighbor[1])) # P
        clause2 = int(str(5) + str(neighbor[0]) + str(neighbor[1])) # W
        negative_alpha = [[clause1,clause2]]
        if KB.Resolution(negative_alpha): # Chắc chắn an toàn
            safe_rooms.append(neighbor)
            KB.add_clause([-clause1])
            KB.add_clause([-clause2])
        elif KB.Resolution([[-clause1]]): # Chắc chắn có Pit
            pit_rooms.append(neighbor)
            KB.add_clause([clause1])
        elif KB.Resolution([[-clause2]]): # Chắc chắn có wumpus
            wumpus_rooms.append(neighbor)
    return KB, safe_rooms, wumpus_rooms, pit_rooms, neighbors, out_of_caves

def IdentifyRoom(KB, heuristic, agent_pos, cave, safe_rooms, list_agent_pos,n):
    '''
    Xác định phòng sẽ đi trong các phòng an toàn
    '''
    heuristic1 = copy.deepcopy(heuristic)
    sub_heuristic = {}
    for safe_room in safe_rooms:
        if safe_room not in heuristic1.keys():
            heuristic1[safe_room] = 0
    # Hạn chế việc đi lại bước cũ, trừ trường hợp ô đang đứng là Breeze(Đã fail vì cơ bản là nó đã k đi lại ô cũ rồi)
    parent_pos = (1,1)
    state = KB.Resolution([[int(str(4) + str(parent_pos[0]) + str(parent_pos[1]))]])
    if len(list_agent_pos) > 1:
        parent_pos = list_agent_pos[-2]
    if parent_pos in safe_rooms:
        heuristic1[parent_pos] -= 1
    if existBreeze(agent_pos, cave,n) and state and parent_pos in safe_rooms:
        heuristic1[parent_pos] -= 1
    for safe_room in safe_rooms:
        sub_heuristic[safe_room] = heuristic1[safe_room]
    room = max(sub_heuristic, key=sub_heuristic.get)
    heuristic1[room] -= 1
    return heuristic1, room