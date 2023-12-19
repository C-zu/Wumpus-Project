from KnowledgeBase import *
import numpy as np
from Agent import *
from Room import *

def Solve_Wumpus_World(agent_pos, agent_direction, n,cave):
    '''
        Mục tiêu: Ăn hết vàng và giết hết Wumpus
    '''
    # Khởi tạo
    origin_agent = agent_pos # Vị trí ban đầu của agent
    cave1 = np.copy(cave) # Dùng np.copy để chống bị ghi đè
    KB = KnowledgeBase() # Knowledge Base
    list_agent_pos = [agent_pos]
    score = 0 # Điểm
    heuristic = {} # Lưu heuristic của các room đã đi vào
    path = [agent_pos] # Lưu đường đi và hành động tại ô đó
    # Tìm vàng thôi
    count = 300
    while(count):           
        # Tìm tất cả các phòng an toàn để tiến hành di chuyển
        KB, safe_rooms, wumpus_rooms, pit_rooms, neighbors = Identify_Safe_Rooms(KB, agent_pos, cave1, n)
        # Nếu 1 vài ô xung quanh là Wumpus thì bắn
        if len(wumpus_rooms) != 0:
            for wumpus_room in wumpus_rooms:
                agent_direction, path = IsTurn(agent_pos, wumpus_room, agent_direction, path)
                cave1, score, state, delete_list = Shoot(KB, room, cave1, n, score)
                path.append(Action.SHOOT)
                if delete_list:
                    path.append(delete_list)
        # Bắn dò
        if existStench(agent_pos, cave1) and len(safe_rooms) < len(neighbors):
            # Những phòng không chắc nó có phải Wumpus hay không
            other_rooms = list(set(neighbors) - set(safe_rooms)|(set(wumpus_rooms)))
            for room in other_rooms:
                agent_direction, path = IsTurn(agent_pos, room, agent_direction, path)
                cave1, score, state, delete_list = Shoot(KB, room, cave1, n, score)
                path.append(Action.SHOOT)
                if delete_list:
                    path.append(delete_list)
                if state:
                    safe_rooms += [room]
                if not existStench(agent_pos, cave1):
                    break
        # Nếu 1 vài ô xung quanh là Pit
#         for pit in pit_rooms:
#             heuristic[pit] = -1000
        # Xác định phòng cần 
        heuristic, room = IdentifyRoom(heuristic,safe_rooms,list_agent_pos)
        # Tiến hành di chuyển
        agent_direction, path = IsTurn(agent_pos, room, agent_direction, path)
        agent_pos, cave1, score, state_bump = Move_Forward(agent_pos, agent_direction, cave1, score)
        path.append(room)
        list_agent_pos.append(room)
        # Nếu tại ô đó có vàng thì ta thu thập
        if existGold(agent_pos, cave1):
            cave1, score = Grab(agent_pos, cave1, score)
            path.append(Action.GRAB)
        count -= 1
    return KB, heuristic, path, list_agent_pos, cave1, score