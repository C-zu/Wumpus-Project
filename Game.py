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
    list_pit = [] # Lưu trữ danh sách các hố
    count_wumpus = 0
    # Tìm vàng thôi
    count = 0
    count_arrow = 0
    while(True):
        count += 1
        # print(agent_pos, agent_direction)
        # Nếu ô bắt đầu có Breeze hay Stench, nhảy ra khỏi động cho an toàn
        if existStench(origin_agent, cave1,n) or existBreeze(origin_agent, cave1,n):
            score = Climb(score)
            path.append(Action.CLIMB)
            print('CLIMB')
            return KB, heuristic, path, list_agent_pos, cave1, score
        # Đã giết được hết Wumpus và ăn hết vàng
        if len(set(list_agent_pos)) + len(list_pit) == n**2:
            print('Số bước đi: ', count)
            print('Số lần bắn: ', count_arrow)
            print('Pit: ', list_pit)
            print('Số lượng wumpus: ', count_wumpus)
            print(len(set(list_agent_pos)))
            return KB, heuristic, path, list_agent_pos, cave1, score
        # Tìm tất cả các phòng an toàn để tiến hành di chuyển
        KB, safe_rooms, wumpus_rooms, pit_rooms, neighbors, out_of_caves = Identify_Safe_Rooms(KB, agent_pos, cave1, n)
        # Nêu phát hiện ra Pit mới, tiến hành thêm vào list_pit
        list_pit += pit_rooms
        list_pit = list(set(list_pit))
        if existBreeze(agent_pos, cave1,n):
            heuristic[agent_pos] -= 1
        # Khi ô đó là Stench thì tiến hành bắn dò để giết Wumpus
        if existStench(agent_pos, cave1,n) and len(safe_rooms) < len(neighbors):
            # Những phòng không chắc nó có phải Wumpus hay không
            other_rooms = list(set(neighbors) - set(safe_rooms))
            for room in other_rooms:
                agent_direction, path = IsTurn(agent_pos, room, agent_direction, path)
                cave1, score, state, delete_list = Shoot(KB, room, cave1, n, score)
                count_arrow += 1
                if state:
                    count_wumpus += 1
                path.append(Action.SHOOT)
                if delete_list:
                    path.append(delete_list)
                if state:
                    safe_rooms += [room]
                if not existStench(agent_pos, cave1,n):
                    break
        # Xác định phòng tiếp theo
        heuristic, room = IdentifyRoom(KB, heuristic,agent_pos, cave1, safe_rooms,list_agent_pos,n)
        # Tiến hành di chuyển
        agent_direction, path = IsTurn(agent_pos, room, agent_direction, path)
        agent_pos, cave1, score, state_bump = Move_Forward(agent_pos, agent_direction, cave1, score, n)
        path.append(room)
        list_agent_pos.append(agent_pos)
        # Nếu tại ô đó có vàng thì ta thu thập
        if existGold(agent_pos, cave1,n):
            cave1, heuristic, score = Grab(agent_pos, cave1, heuristic, score, n)
            path.append(Action.GRAB)
