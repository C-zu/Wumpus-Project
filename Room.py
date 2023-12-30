from config import *
from Percept import *
from KnowledgeBase import *
import copy


def Info_Room(pos, cave,n):
    '''
        Info room tại vị trí của agent đang đứng.
    '''
    pos = map_pos(pos,n) # Chuyển đổi Pos để phù hợp với Numpy
    x,y  = pos 
    # Gán giá trị
    info_room = {'Stench': 0, 'Breeze':0, 'Gold': 0}
    if 'S' in cave[x, y]:
        info_room['Stench'] = 1
    if 'B' in cave[x,y]:
        info_room['Breeze'] = 1
    if 'G' in cave[x, y]:
        info_room['Gold'] = 1
    return info_room

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


def Literals_Room(pos):
    x, y = pos
    info_map = {'Pit': '4', 'Wumpus': '5'}
    list_literals = []
    for name, value in info_map.items():
        literal = [- int(value + str(x) + str(y))]
        list_literals.append(literal)
    return list_literals


def is_delete(KB_temp,CNF):
    for literal in CNF:
        if [-literal] not in KB_temp:
            return False
    return True

def delete_KB(KB):
    for CNF in KB.KB:
        if len(CNF) > 1 and is_delete(KB.KB,CNF):
            KB.del_clause(CNF)
    return KB

def get_clauses_in_KB(KB, pos):
    '''
    Lấy ra tất cả những clause liên quan đến pos có trong KB
    '''
    list_clauses = []
    literial1 = int(str(4) + str(pos[0]) + str(pos[1]))
    literial2 = int(str(5) + str(pos[0]) + str(pos[1]))
    for clause in KB:
        if (literial1 in clause) or (-literial1 in clause) or (literial2 in clause) or (-literial2 in clause):
            list_clauses.append(clause)
    return list_clauses
def filter_KB(list_KB, neighbor,n):
    additional_KB = get_clauses_in_KB(list_KB, neighbor)
    neighbors = get_neighbors(neighbor, n)
    for sub_neighbor in neighbors:
        additional_KB += get_clauses_in_KB(list_KB, sub_neighbor)
    return additional_KB

def Identify_Safe_Rooms( KB, agent_pos, cave, n):
    list_CNF = [Literals_Room(agent_pos)]
    list_new_KB = [Literals_Room(agent_pos)]
    if NoSB(agent_pos, cave,n):
        list_CNF.append(Not_SB_Case(agent_pos, n))
        list_new_KB.append(Not_SB_Case(agent_pos, n))
    if existStench(agent_pos, cave,n):
        list_CNF.append(Stench_Case(agent_pos, n))
        list_new_KB.append(Stench_Case(agent_pos, n))
    if existBreeze(agent_pos, cave,n):
        list_CNF.append(Breeze_Case(agent_pos, n))
        list_new_KB.append(Breeze_Case(agent_pos, n))
    for CNF_i in list_CNF:
        for clause in CNF_i:
            KB.add_clause(clause)
    KB = delete_KB(KB)
    # Get neighbors
    neighbors= get_neighbors(agent_pos, n)
    # Tiến hành loại bỏ các KB vô nghĩa để tăng thời gian xử lí
    new_KB = KnowledgeBase()
    for neighbor in neighbors:
        list_new_KB.append(filter_KB(KB.KB, neighbor,n))
    for KB1 in list_new_KB:
        for clause in KB1:
            new_KB.add_clause(clause)
    # Xác định các ô an toàn để đi
    safe_rooms = []
    wumpus_rooms = []
    pit_rooms = []
    for neighbor in neighbors:
        clause1 = int(str(4) + str(neighbor[0]) + str(neighbor[1])) # P
        clause2 = int(str(5) + str(neighbor[0]) + str(neighbor[1])) # W
        negative_alpha = [[clause1,clause2]]
        if new_KB.Resolution(negative_alpha): # Chắc chắn an toàn
            safe_rooms.append(neighbor)
            KB.add_clause([-clause1])
            KB.add_clause([-clause2])
        elif new_KB.Resolution([[-clause1]]): # Chắc chắn có Pit
            pit_rooms.append(neighbor)
            KB.add_clause([clause1])
        elif new_KB.Resolution([[-clause2]]): # Chắc chắn có wumpus
            wumpus_rooms.append(neighbor)
    return KB, safe_rooms, wumpus_rooms, pit_rooms, neighbors

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
    state = KB.Resolution([[int(str(4) + str(parent_pos[0]) + str(parent_pos[1]))]]) # Không có hố thì trả về True
    if len(list_agent_pos) > 1:
        parent_pos = list_agent_pos[-2]
    # Dùng để hạn chế đi lại bước cha
    # if parent_pos in safe_rooms:
    #     heuristic1[parent_pos] -= 1
    if existBreeze(agent_pos, cave,n) and state and parent_pos in safe_rooms:
        heuristic1[parent_pos] -= 1
    for safe_room in safe_rooms:
        sub_heuristic[safe_room] = heuristic1[safe_room]
    room = max(sub_heuristic, key=sub_heuristic.get)
    heuristic1[room] -= 1 # Heuristic -1 sau mỗi bước
    return heuristic1, room
