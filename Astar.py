# Hàm A* với heuristic
from config import *
def astar_with_heuristic(matrix, start, goal, pit_rooms):
    def heuristic(a, b):
        # Hàm ước lượng chi phí (heuristic) sử dụng khoảng cách Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    rows = len(matrix)
    cols = len(matrix[0])

    open_set = {start}
    came_from = {}
    g_score = {position: float('inf') for position in [(i, j) for i in range(1,rows+1) for j in range(1,cols+1)]}
    g_score[start] = 0
    f_score = {position: float('inf') for position in [(i, j) for i in range(1,rows+1) for j in range(1,cols+1)]}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        for neighbor in get_neighbors(current, rows, cols, pit_rooms):
            tentative_g_score = g_score[current] + 1  # Trọng số đơn giản, có thể thay đổi tùy theo yêu cầu

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None

# Hàm lấy các đỉnh hàng xóm
def get_neighbors(pos, rows, cols, pit_rooms):
    new_pit_rooms = [map_pos(x,rows) for x in pit_rooms]
    neighbors = []
    deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for delta in deltas:
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])
        if 1 <= new_pos[0] <= rows and 1 <= new_pos[1] <= cols:
            new_set = (new_pos[0],new_pos[1])
            if map_pos(new_set,rows) not in new_pit_rooms:
                neighbors.append(new_pos)
    return neighbors

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))