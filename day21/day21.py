from collections import defaultdict
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

part1 = 0
part2 = 0

board = []

#with open("test.txt") as file:
with open("day21.txt") as file:
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        row = []
        for x,ch in enumerate(line):
            if ch == "S":
                start = (x,y)
            row.append(ch)
        board.append(row)

W = len(board[0])
H = len(board)

def walk1(board, x, y, W, H, steps):
    visited = set()
    can_visit = set()
    Q = [(x,y,0)]
    can_visit.add((0,0))

    while Q:
        cx, cy, cs = Q.pop(0)
        visited.add((cx,cy,cs))
        for dx,dy in [(0,1), (0,-1), (1,0), (-1, 0)]:
            nx = cx + dx
            ny = cy + dy
            ns = cs + 1
            if nx < 0 or ny < 0 or nx >= W or ny >= H:
                continue

            if board[ny][nx] == "#":
                continue
            can_visit.add((nx,ny))

            if (nx,ny) not in visited:
                Q.append((nx,ny,ns + 1))

        print("min of ", min([x[2] for x in Q]))
        if all([x[2] > steps for x in Q]):
            return can_visit

def walk(board, x, y, W, H, steps):
    visited = set()
    can_visit = set()
    Q = [(x,y,0)]
    can_visit.add((0,0))

    while Q:
        cx, cy, cs = Q.pop(0)
        visited.add((cx,cy,cs))
        for dx,dy in [(0,1), (0,-1), (1,0), (-1, 0)]:
            nx = cx + dx
            ny = cy + dy
            ns = cs + 1
            if nx < 0 or ny < 0 or nx >= W or ny >= H:
                continue

            if board[ny][nx] == "#":
                continue
            
            Q.append((nx,ny,ns + 1))

        print("min of ", min([x[2] for x in Q]))
        if all([x[2] > steps for x in Q]):
            return Q
import heapq    
# could send in the farther away and keep track of nodes we pass through
# then smalelr searches are likley to be cached
def can_reach(board, start, goal, W, H, steps):
    Q = []
    dist = {}
    # for y in range(H):
    #     for x in range(W):
    #         dist[(x,y)] = steps + 1
    heapq.heappush(Q, (0, start[0], start[1],))

    while Q:
        cs, cx, cy = Q.pop(0)
        if (cx,cy) in dist:
            continue
        dist[(cx,cy)] = cs

        for dx,dy in [(0,1), (0,-1), (1,0), (-1, 0)]:
            nx = cx + dx
            ny = cy + dy
            ns = cs + 1

            if ns > steps:
                continue

            if nx < 0 or ny < 0 or nx >= W or ny >= H:
                continue

            if board[ny][nx] == "#":
                continue
            
            if (nx,ny) == goal:
                return True
            
            if (nx,ny) in dist:
                continue

            heapq.heappush(Q, (ns, nx, ny))

    return False

def manhattan_distance(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def paint_board(board, W, H, start, steps, perimiter_thickness = 2):
    perimiter = defaultdict(list)
    for y in range(H):
        # if steps % 2 == 0:
        #     startx = 0 if y % 2 == 0 else 1
        # else:
        #     startx = 0 if y % 2 == 1 else 1
        for x in range(W):
            if manhattan_distance((x,y), start) <= steps:
                if board[y][x] != "#":
                    #board[y][x] = "O"
                    perimiter[y].append((x,y))
                    # if len(perimiter[y]) == perimiter_thickness:
                    #     perimiter[y].pop(perimiter_thickness // 2)

    return perimiter
# visited = walk(board, start[0], start[1], W, H, 6+1)
# vxy = [(x[0],x[1]) for x in visited]
STEPS = 64
candidates = paint_board(board, W, H, start, STEPS, 1e6) 
for y in range(H):
    for x in range(W):
        print(board[y][x] if (x,y) not in candidates[y] else "O", end="")
    print()

def generate_candidates(board, start, W, H, steps):
    sources = [start]
    for i in range(steps):
        print(i)
        next_sources = []
        candidates = set()
        for cur in sources:
            for dx,dy in [(0,1), (0,-1), (1,0), (-1, 0)]:
                nx = cur[0] + dx
                ny = cur[1] + dy
                if nx < 0 or ny < 0 or nx >= W or ny >= H:
                    continue
                if board[ny][nx] == "#":
                    continue
                if (nx,ny) in candidates:
                    continue
                next_sources.append((nx,ny))
                candidates.add((nx,ny))
        sources = next_sources
    candidates.add(start)
    return candidates

c = generate_candidates(board, start, W, H, STEPS)
can_see = set()
for coord in c:
    if can_reach(board, start, coord, W, H, STEPS):
        can_see.add(coord)
        part1 += 1
# for y in paint_board(board, W, H, start, STEPS-1, 1e6):
#     print("y = ",y,len(candidates[y]))
#     for coord in candidates[y]:
#         if coord not in can_see and can_reach(board, start, coord, W, H, STEPS-1):
#             part1 += 1

answer(part1)
#answer(part2)
