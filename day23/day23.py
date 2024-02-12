from collections import defaultdict
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

dirs = {
    ">": [(1,0)],
    "<": [(-1,0)],
    "v": [(0,1)],
    "^": [(0,-1)]
}
part1 = 0
part2 = 0

board = []
start = None
goal = None
#with open("test.txt") as file:
with open("day23.txt") as file:
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        board.append(list(line))

# find start
start = (board[0].index("."), 0)
goal = (board[-1].index("."), len(board)-1)

W = len(board[0])
H = len(board)

print (start, goal, W,H)

def get_max(Q):
    if not Q:
        return None
    
    max_val = Q[0][0]
    max_index = 0
    for i in range(1, len(Q)):
        if Q[i][0] > max_val:
            max_val = Q[i][0]
            max_index = i
    return max_index

def can_reach(board, start, goal, W, H, ignore_slopes=False):
    Q = []
    dist = defaultdict(lambda: 0)
    visisted = set()
    prev = defaultdict(lambda: None)

    # if ignore_slopes:
    #      visisted.add((goal[0],goal[1],dirs["^"][0]))
    #      heapq.heappush(Q, (0, start[0], start[1], dirs[""][0]))
    #  else:
    visisted.add((start[0],start[1],dirs["v"][0]))
    Q.append((0, start[0], start[1], dirs["v"][0]))
    paths = []
    while Q:
        next_index = get_max(Q)
        cs, cx, cy, cdir = Q.pop(next_index)
        visisted.add((cx,cy,cdir))

        if ignore_slopes:
            available_dirs = [(0,1), (0,-1), (1,0), (-1, 0)]
        else:
            available_dirs = dirs.get(board[cy][cx], [(0,1), (0,-1), (1,0), (-1, 0)])
        for dx,dy in available_dirs:
            nx = cx + dx
            ny = cy + dy
            ns = cs + 1

            if (dx,dy) == (-cdir[0], -cdir[1]):
                continue

            if nx < 0 or ny < 0 or nx >= W or ny >= H:
                continue

            if board[ny][nx] == "#":
                continue
            
            # if (nx,ny,(dx,dy)) in visisted:
            #     continue

            if (nx,ny) == goal:
                paths.append((ns,nx,ny))

            if ns > dist[(nx,ny)] and (nx,ny,(dx,dy)) not in visisted:
                dist[(nx,ny)] = ns
                prev[(nx,ny)] = (cx,cy)
                #heapq.heappush(Q, (ns, nx, ny))
                Q.append((ns, nx, ny, (dx,dy)))

    path = [goal]
    # c = goal
    # while prev[c]:
    #     path.append(prev[c])
    #     c = prev[c]

    return max([x[0] for x in paths]) if paths else None, reversed(path)


#part1, path = can_reach(board, start, goal, W, H)
answer(part1)

## part two make it a graph of junctions
vertices = set()
graph = defaultdict(list)

for y in range(1,H-1):
    for x in range(1,W-1):
        if board[y][x] == "#":
            continue

        junction = 0
        for dx,dy in [(0,1), (0,-1), (1,0), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            if board[ny][nx] != "#":
                junction += 1

        if junction > 2:
            vertices.add((x,y))
            print("Junction at: ",x,y, junction)

#Construct edges
def find_junction_or_goal(start, dir, end, count, board, W, H, visited=set()):
    q = [(start[0], start[1], dir[0], dir[1], count)]
    while q:
        x, y, dx, dy, d = q.pop()
        if (x,y) == end:
            return [((x, y), d)]
        visited.add((x,y))

        for ndx,ndy in [(0,1), (0,-1), (1,0), (-1, 0)]:
            if (ndx, ndy) == (-dx, -dy):
                continue
            nx = x + ndx
            ny = y + ndy
            nd = d + 1
            if 0 <= nx < W and 0 <= ny < H and board[ny][nx] != "#" and (nx,ny) not in visited:
                q.append((nx,ny,ndx,ndy,nd))

        if len(q) > 1:
            print("@Junction", x,y)
            return [((d[0],d[1]), (d[2],d[3]), d[4]) for d in q] 

    return []       

def build_graph(graph, start, dir, end, count, board, W, H, visited):
    print('build graph', start, dir, count)
    dx,dy = dir    
    x,y = start
    visited.add((x,y))
    while True:
        # now go to a junction
        if start == end:
            return # done!

        options = []
        for ndx,ndy in [(0,1), (0,-1), (1,0), (-1, 0)]:
            # Don't go backwards
            if (ndx,ndy) == (-dx,-dy):
                continue

            nx = x + ndx
            ny = y + ndy
            if 0 <= nx < W and 0 <= ny < H and board[ny][nx] != "#" and (nx,ny) not in visited:
                options.append((nx,ny,ndx,ndy,count+1))

        # hit dead end, stop!
        if not options:
            return
        
        # if we have a path forward, continue, and try all other options
        x,y,dx,dy,count = options[0]
        visited.add((x,y))

        if len(options) > 1:
            jx = x - dx
            jy = y - dy
            jc = count - 1
            visited.add((jx,jy))
            graph[start].append((jx, jy, jc))
            for opt in options[1:]:
                jx,jy,jdx,jdy,jc = opt     
                build_graph(graph, (jx, jy), (jdx, jdy), end, jc, board, W, H, set(list(visited)))

def dfs(graph, cur, goal, pathset, dist):
    print('dfs', cur, dist)
    global part2
    if cur == goal:
        part2 = max(part2, dist)
    for v in graph[cur]:
        cur, d = v
        if cur not in pathset:
            pathset.add(cur)
            dfs(graph, cur, goal, pathset, dist+d)
            pathset.remove(cur)

g = defaultdict(list)
q = [((start[0], start[1]+1), (0,1), 0)]
visited = set()
while q:
    cur, dir, d = q.pop(0)
    jx = find_junction_or_goal(cur, dir, goal, 0, board, W, H, visited)
    cur = (cur[0] - dir[0], cur[1] - dir[1])    
    if not jx:
        continue

    if len(jx) == 1:
        x,y = jx[0][0]
        assert x == goal[0] and y == goal[1]        
        p,d = jx[0]
        graph[cur].append((p, d))
    else:
        p,dir,d = jx[0]
        print(f"{len(jx)} {cur} --> {(p[0]-dir[0],p[1]-dir[1])} {jx}")
        graph[cur].append(((p[0]-dir[0],p[1]-dir[1]), d))
        for j in jx:
            q.append(j)

print(graph)
dfs(graph, start, goal, set(), 0)
print(part2)
exit()
print(graph)
exit()
build_graph(g, start, (0,1), goal, 0, board, W, H, set())
print(g)
exit()
vertices = list(vertices)
vertices.append(start)
vertices.append(goal)
print(len(vertices),"junctions")
for i in range(len(vertices)):
    print(i, len(vertices))
    for j in range(i+1, len(vertices)):
        dist, path = can_reach(board, vertices[i], vertices[j], W, H, True)
        if dist:
            graph[vertices[i]].append((dist, vertices[j]))

#part2, path = can_reach(board, start, goal, W, H, ignore_slopes=True)
answer(part2)
print(graph)
print(graph[start])
print(goal)
for n in graph[start]:
    if n[1] == goal:
        print("Found", n[0])
    
exit()

#2216 too low

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
STEPS = 26501365 #64
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
