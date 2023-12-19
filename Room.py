from config import *
from Percept import *
import copy


def Info_Room(pos, cave):
    '''
        Info room tại vị trí của agent đang đứng.
    '''
    pos = map_pos(pos) # Chuyển đổi Pos để phù hợp với Numpy
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


def existStench(agent_pos, cave):
    info_room = Info_Room(agent_pos, cave)
    return info_room['Stench'] == 1
def existBreeze( agent_pos, cave):
    info_room = Info_Room(agent_pos, cave)
    return info_room['Breeze'] == 1
def existGold( agent_pos, cave):
    info_room = Info_Room(agent_pos, cave)
    return info_room['Gold'] == 1
def NoSB( agent_pos, cave):
    info_room = Info_Room(agent_pos, cave)
    return (info_room['Stench'] == 0 and info_room['Breeze'] == 0)


def Identify_Safe_Rooms( KB, agent_pos, cave, n):
    info_room = Info_Room(agent_pos,cave)
    list_CNF = [Literals_Room(info_room, agent_pos)]
    if NoSB(agent_pos, cave): 
        list_CNF.append(Not_SB_Case(agent_pos, n))
    if existStench(agent_pos, cave):
        list_CNF.append(Stench_Case(agent_pos, n))
    if existBreeze(agent_pos, cave):
        list_CNF.append(Breeze_Case(agent_pos, n))
    for CNF_i in list_CNF:
        for clause in CNF_i:
            KB.add_clause(clause)
    # Xác định các ô an toàn để đi
    safe_rooms = []
    pit_rooms = []
    neighbors, out_of_caves = get_neighbors(agent_pos, n)
    for neighbor in neighbors:
        clause1 = int(str(4) + str(neighbor[0]) + str(neighbor[1])) # P
        clause2 = int(str(5) + str(neighbor[0]) + str(neighbor[1])) # W
        negative_alpha = [[clause1,clause2]]
        if KB.Resolution_Algorithm(negative_alpha): # Chắc chắn an toàn
            safe_rooms.append(neighbor)
        elif KB.Resolution_Algorithm([[-clause1]]): # Chắc chắn có Pit
            pit_rooms.append(neighbor)
    return KB, safe_rooms, pit_rooms, neighbors, out_of_caves


def Heuristic_Rooms(heuristic, safe_rooms, list_agent_pos):
    '''
    Heuristic của tất cả các phòng agent nhận thức được là nó an toàn
    '''
    heuristic1 = copy.deepcopy(heuristic)
    for safe_room in safe_rooms:
        if safe_room not in heuristic1.keys():
            heuristic1[safe_room] = 0
    return heuristic1


def IdentifyRoom(heuristic, safe_rooms, list_agent_pos):
    '''
    Xác định phòng sẽ đi trong các phòng an toàn
    '''
    heuristic1 = copy.deepcopy(heuristic)
    heuristic1 = Heuristic_Rooms(heuristic1, safe_rooms, list_agent_pos)
    sub_heuristic = {}
    for safe_room in safe_rooms:
        sub_heuristic[safe_room] = heuristic1[safe_room] 
    room = max(sub_heuristic, key = sub_heuristic.get)
    heuristic1[room] -= 1
    return heuristic1, room