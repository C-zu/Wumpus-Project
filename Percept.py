def get_neighbors(pos, n):
    '''
    Kiểm tra những ô xung quanh
    '''
    neighbors = []
    out_of_caves = []
    for dx, dy in [(1, 0), (-1,0), (0, 1), (0, -1)]:
        x, y = pos[0] + dx, pos[1] + dy
        if (1 <= x <= n and 1 <= y <= n):
            neighbors.append((x, y))
        else:
            out_of_caves.append((x,y))
    return neighbors, out_of_caves


def Not_SB_Case(pos, n):
    neighbors, _ = get_neighbors(pos, n)
    CNF = []
    for neighbor in neighbors:
        literal1 = [int('-4' + str(neighbor[0]) + str(neighbor[1]))]
        literal2 = [int('-5' + str(neighbor[0]) + str(neighbor[1]))]
        CNF.append(literal1)
        CNF.append(literal2)
    return CNF
# Ô đang đứng có Stench
def Stench_Case(pos, n):
    neighbors, _ = get_neighbors(pos, n)
    # clause 1
    clause1 = []
    for neighbor in neighbors:
        literal1 = int('5' + str(neighbor[0]) + str(neighbor[1]))
        clause1.append(literal1)
    return [clause1]
# Ô đang đứng có Breeze
def Breeze_Case(pos, n):
    neighbors, _ = get_neighbors(pos, n)
    # clause 1
    clause1 = []
    for neighbor in neighbors:
        literal1 = int('4' + str(neighbor[0]) + str(neighbor[1]))
        clause1.append(literal1)
    return [clause1]