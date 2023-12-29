from KnowledgeBase import *
from Agent import *
from Room import *
from Astar import *
import numpy as np
# Nếu có 1 ô đã đi nhiều hơn 5 lần thì tiến hành quay về nhà
def stop_condition(list_agent_pos,n):
    count_stop = {}
    for pos in list_agent_pos:
        if pos not in count_stop.keys():
            count_stop[pos] = 0
        else:
            count_stop[pos] += 1
    result = [key for key, value in count_stop.items() if value >= n]
    return len(result)>0
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
        # Nếu tại ô đó có vàng thì ta thu thập
        if existGold(agent_pos, cave1,n):
            cave1, heuristic, score = Grab(origin_agent, agent_pos, cave1, heuristic, score, n)
            path.append(Action.GRAB)
        # Nếu ô bắt đầu có Breeze hay Stench, nhảy ra khỏi động cho an toàn
        if existStench(origin_agent, cave1,n) or existBreeze(origin_agent, cave1,n):
            score = Climb(score)
            path.append(Action.CLIMB)
            print('CLIMB')
            return KB, heuristic, path, list_agent_pos, cave1, score
        # Nếu đi lâu mà không thu được gì thì tiến hành quay về để CLIMB
        if stop_condition(list_agent_pos,n):
            path_back = astar_with_heuristic(cave, agent_pos, origin_agent, list_pit)
            path += path_back
            score = Climb(score)
            path.append(Action.CLIMB)
            print('CLIMB')
            return KB, heuristic, path, list_agent_pos, cave1, score
        # Đã giết được hết Wumpus và ăn hết vàng
        if len(set(list_agent_pos)) + len(list_pit) == n**2:
            print('Số bước đi: ', count)
            print('Số lần bắn: ', count_arrow)
            print('Số lượng Pit: ', len(list_pit))
            print('Số lượng wumpus: ', count_wumpus)
            # Tìm đường quay về origin_agent
            path_back = astar_with_heuristic(cave, agent_pos, origin_agent, list_pit)
            path += path_back
            print(path_back)
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
