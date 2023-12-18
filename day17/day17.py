import sys
sys.setrecursionlimit(10**6)
import heapq

###
#   Submission helper, print the answer and copy it to the clipboard
#   to reduce the amount of times I have the answer and mistype it :).
###
#import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    #pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

def show_map(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            print(board[y][x], end="")
        print()

part1 = 0
part2 = 0

start = (0,0)
dir = (1,0)

N_dir,E_dir,S_dir,W_dir = ((0,-1), (1,0), (0,1), (-1, 0))

def get_right_dir(dir):
    if dir == N_dir:
        return E_dir
    if dir == E_dir:
        return S_dir
    if dir == S_dir:
        return W_dir
    if dir == W_dir:
        return N_dir

def get_left_dir(dir):
    if dir == N_dir:
        return W_dir
    if dir == E_dir:
        return N_dir
    if dir == S_dir:
        return E_dir
    if dir == W_dir:
        return S_dir
    
def get_reachable(node, W, H):
    reachable = []
    x,y = node[0]
    dx,dy = node[1]
    moves_left = node[2]

    # left
    lx, ly = get_left_dir(dir)
    llx = x + lx
    lly = y + ly
    if 0 <= llx < W and 0 <= lly < H:
        reachable.append(((llx, lly), (lx,ly), 2))
    # right
    rx, ry = get_right_dir(dir)
    rrx = x + rx
    rry = y + ry
    if 0 <= rrx < W and 0 <= rry < H:
        reachable.append(((rrx, rry), (rx,ry), 2))    

    # straight
    if moves_left > 0 and 0 <= x+dx < W and 0 <= y+dy < H:
        reachable.append(((x+dx, y+dy), dir, moves_left - 1))

    return reachable

# def get_reachable(node, W, H):
#     reachable = []
#     x,y = node[0]
#     dx,dy = node[1]
#     moves_left = node[2]   
#     # left 
#     reachable.append(((x,y), get_left_dir((dx,dy)), 3))
#     # right
#     reachable.append(((x,y), get_right_dir((dx,dy)), 3))
#     # straight
#     if moves_left > 0 and 0 <= x+dx < W and 0 <= y+dy < H:
#         reachable.append(((x+dx, y+dy), dir, moves_left - 1))
#     return reachable

from collections import defaultdict
import math

def get_min(q,dist):
    min_dist = dist[(q[0][0], q[0][1])]
    min_index = 0
    for n in range(1, len(q)):
        d = dist[(q[n][0], q[n][1])]
        if d < min_dist:
            min_dist = d
            min_index = n
    return min_index

def djiksra(board, start, goal):
    W = len(board[0])
    H = len(board)

    q = []
    for y in range(0,H):
        for x in range(0,W):
            for ml in range(3,4):
                q.append(((x,y), N_dir, ml))
                q.append(((x,y), E_dir, ml))
                q.append(((x,y), S_dir, ml))
                q.append(((x,y), W_dir, ml))

    visited = set()
    distance = defaultdict(lambda: math.inf)
    distance[((0,0), N_dir)] = 0
    distance[((0,0), E_dir)] = 0
    distance[((0,0), S_dir)] = 0
    distance[((0,0), W_dir)] = 0
    prev = defaultdict(lambda: None)
             
    q = [(start, E_dir, 2), (start, S_dir, 2)]
    #heapq.heappush(q, (0, (start, E, 3)))
    while q:
        #cur = heapq.heappop(q)
        node_index = get_min(q, distance)
        node = q[node_index]
        q.remove(node)

        pos, dir, moves_left = node
        visited.add(pos)
        for r in get_reachable(node, W, H):
            r_pos, r_dir, r_moves_left = r
            assert r_moves_left < 4

            # if r in visited:
            #     continue
            # movement contraint
            # test for 3 in a row?
            in_a_row = 0
            # onto something here
            p_next = r_pos
            p = pos
            while p and in_a_row <= 3:
                drx = p_next[0] - p[0]
                dry = p_next[1] - p[1]
                if (drx,dry) == r_dir:
                    in_a_row += 1
                p_next = p
                p = prev[p]
            print("iar", in_a_row)
            alt = distance[(pos,dir)] + board[r_pos[1]][r_pos[0]] #+ (0 if in_a_row < 3 else (W*H)**16)
                    
            if alt < distance[(r_pos, r_dir)] and in_a_row < 3:
                distance[(r_pos, r_dir)] = alt 
                prev[(r_pos, r_dir)] = pos
            # else:
            #     assert r_pos != goal, alt
            if r_pos not in visited and in_a_row < 3:
            #     print("Adding", r)
                q.append(r)
            #     heapq.heappush(q, (alt, r))
            
    heat_loss = board[goal[1]][goal[0]]
    path = [goal]
    current = goal
    while prev[current]:
        x,y = current
        heat_loss += board[y][x]
        path.append(prev[current])
        current = prev[current]
    #assert current == start

    # dont incur heat loss from 0,0
    heat_loss -= board[0][0]
    return heat_loss, list(reversed(path))

class Node():
    def __init__(self, position=None, parent=None, direction=E_dir, moves_left=3):
        if not position:
            raise Exception("Position must be specified")

        self.position = position
        self.parent = parent
        self.dir = direction
        self.moves_left = moves_left

        if (parent is None):
            self.distance_from_start = 0
        else:
            self.distance_from_start = parent.distance_from_start + 1
        self.distance_from_target = 0
        self.cost = 0

    def __eq__(self, other):
        return self.position == other.position


def get_squared_distance(first, second):
    squared_x_distance = (first.position[0] - second.position[0]) ** 2
    squared_y_distance = (first.position[1] - second.position[1]) ** 2

    return squared_x_distance + squared_y_distance


def get_path_from_node(node):
    path = []
    while node is not None:
        path.append(node.position)
        node = node.parent
    return path[::-1]


def is_invalid_position(maze, node):
    if (node.position[0] >= len(maze[0])):
        return True

    if (node.position[1] >= len(maze)):
        return True

    if (node.position[0] < 0):
        return True

    if (node.position[1] < 0):
        return True

    if (maze[node.position[1]][node.position[0]] != 0):
        return True

    return False

def astar(maze, start_position, end_position):
    W = len(maze[0])
    H = len(maze)
    start_node = Node(start_position)
    end_node = Node(end_position)

    nodes = [start_node]
    visited_nodes = defaultdict(bool)

    while len(nodes) > 0:
        current_index = 0
        for index in range(len(nodes)):
            if nodes[index].cost < nodes[current_index].cost:
                current_index = index

        current_node = nodes[current_index]
        visited_nodes[current_node.position] = True
        nodes.pop(current_index)

        if current_node == end_node:
            return get_path_from_node(current_node)

        for new_node in get_reachable(current_node, W, H):

            if (visited_nodes[new_node.position]):
                continue

            new_node.distance_from_target = get_squared_distance(new_node, end_node)
            new_node.cost = current_node.cost + maze[new_node.position[1]][new_node.position[0]]

            found_in_list = False
            for node in nodes:
                if new_node == node and new_node.distance_from_start > node.distance_from_start:
                    found_in_list = True
                    break

            if (found_in_list):
                continue
            nodes.append(new_node)
    return []

def path(board, start, goal):
    W = len(board)
    H = len(board[0])

    visited = set(start)
    candidates = []
    # loc, dir, moves_left, heat
    n = [(start, E, 3, 0)]
    while n:
        cur, dir, moves_left, heat_loss = n.pop(0)

        if cur in visited:
            continue
        visited.add(cur)

        if cur == goal:
            return heat_loss + board[goal[1]][goal[0]]
        
        candidates = []
        for rn in get_reachable(cur, dir, moves_left, W, H):
            h = board[cur[1]][cur[0]]
            candidates.append(((rn[0],rn[1],rn[2],heat_loss+h), heat_loss+h))
            print (f"trying {rn[0]}, {rn[1]}, {rn[2]} heat = {board[cur[1]][cur[0]]}")

        for x in sorted(candidates, key=lambda x: x[1]):
            n.append(x[0])

    assert False, candidates

board = []
with open("test.txt") as file:
#with open("day17.txt") as file:
    for y,line in enumerate(file.readlines()):
        line = line.strip()
        board.append([int(x) for x in list(line.strip())])

goal = (len(board[0])-1, len(board)-1)
show_map(board)
print(start, goal)
from d import shortest
print(shortest(board, len(board), len(board[0])))
# part1, path = djiksra(board, start, goal)
# #part1 = path(board, start, goal)
# for loc in path: #astar(board, start, goal):
#     part1 += board[loc[1]][loc[0]]
#     board[loc[1]][loc[0]] = "*"
# show_map(board)
# print(path)
# answer(part1)
# #answer(part2)