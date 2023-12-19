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
    count_wumpus = 0
    list_pit = [] # Lưu trữ danh sách các hố
    dict_bump = {} # Lưu trữ số lần Bump
    size_x = 0
    size_y = 0 # Kích thước Cave được suy ra từ Bump
    # Tìm vàng thôi
    count = 0
    while(True):
        count += 1
        # Nếu ô bắt đầu có Breeze hay Stench, nhảy ra khỏi động cho an toàn
        if existStench(origin_agent, cave1) or existBreeze(origin_agent, cave1):
            score = Climb(score)
            path.append(Action.CLIMB)
            print('CLIMB')
            return KB, heuristic, path, list_agent_pos, cave1, score
        # Đã giết được hết Wumpus và ăn hết vàng
        if len(set(list_agent_pos)) + count_wumpus + len(list_pit) == n**2:
            print(count)
            return KB, heuristic, path, list_agent_pos, cave1, score
        # Tìm tất cả các phòng an toàn để tiến hành di chuyển
        KB, safe_rooms, pit_rooms, neighbors, out_of_caves = Identify_Safe_Rooms(KB, agent_pos, cave1, n)
        list_pit += pit_rooms
        list_pit = list(set(list_pit))
        # Bắn dò
        if existStench(agent_pos, cave1) and len(safe_rooms) < len(neighbors):
            # Những phòng không chắc nó có phải Wumpus hay không
            other_rooms = list(set(neighbors) - set(safe_rooms))
            for room in other_rooms:
                agent_direction, path = IsTurn(agent_pos, room, agent_direction, path)
                cave1, score, state, delete_list = Shoot(KB, room, cave1, n, score)
                if state:
                    count_wumpus += 1
                path.append(Action.SHOOT)
                if delete_list:
                    path.append(delete_list)
                if state:
                    safe_rooms += [room]
                if not existStench(agent_pos, cave1):
                    break
        # Xác định phòng tiếp theo
        heuristic, room = IdentifyRoom(heuristic,safe_rooms,list_agent_pos)
        # Trước khi di chuyển thì ta sẽ tiến hành kiểm tra xem ô đó có phải là edge không, nếu là edge thì ta đâm.
        # if len(out_of_caves) == 1:
        #     for ooc in out_of_caves:
        #         agent_direction, path = IsTurn(agent_pos, ooc, agent_direction, path)
        #         agent_pos, cave1, score, state_bump = Move_Forward(agent_pos, agent_direction, cave1, score)
        #         if state_bump:
        #             dict_bump[agent_pos] = agent_direction
        #             if len(set(dict_bump.values())) == 4:
        #                 size_x, size_y = Determine_Cave_Size(dict_bump)
        # Tiến hành di chuyển
        agent_direction, path = IsTurn(agent_pos, room, agent_direction, path)
        agent_pos, cave1, score, state_bump = Move_Forward(agent_pos, agent_direction, cave1, score)
        path.append(room)
        list_agent_pos.append(room)
        # Nếu tại ô đó có vàng thì ta thu thập
        if existGold(agent_pos, cave1):
            cave1, score = Grab(agent_pos, cave1, score)
            path.append(Action.GRAB)
            # heuristic[agent_pos] -= 10

