from collections import defaultdict
from day10_render import render
from helpers import answer

N = 0
E = 1
S = 2
W = 3

moves = {
    # type : NESW
    "|": [True, False, True, False ],
    "-": [False, True, False, True ],

    "L": [True, True, False, False ],
    "J": [True, False, False, True ],
    "7": [False, False, True, True ],
    "F": [False, True, True, False ],

    ".": [False, False, False, False ],
}

m2 = {
    # type : NESW
    "|": { N: N, S: S },
    "-": { E: E, W: W  },

    "L": { W:N, S:E }, 
    "J": { E:N, S:W }, 
    "7": { N:W, E:S }, 
    "F": { N:E, W:S }, 

    ".": { }
}

asciimap = {
    "F": "┌",
    "J": "┘",
    "-": "─",
    "|": "│",
    "7": "┐",
    "L": "└"
}

asciimap2 = {
    "F": "╔",
    "J": "╝",
    "-": "═",
    "|": "║",
    "7": "╗",
    "L": "╚"
}
class Board:
    def __init__(self, file):
        self.board = []
        self.start = None
        with open(file) as file:
            for i, line in enumerate(file.readlines()):        
                line = line.strip()
                if "S" in line:
                    assert self.start == None
                    self.start = (line.index("S"), i)
                row = list(line)
                self.board.append(row)
        self.width = len(self.board[0])
        self.height = len(self.board)

    def get(self, x, y):
        return self.board[y][x]

    def set(self, x, y, ch):
        self.board[y][x] = ch

    def find_starting_dir(self):
        neighbors = self.get_neighbors(self.start)
        if neighbors[N] in "|7F":
            return N
        if neighbors[E] in "-7J":
            return E
        if neighbors[S] in "|LJ":
            return S
        if neighbors[W] in "-FL":
            return W

    def get_neighbors(self, position, print_out=False):
        x,y = position
        # N, E, S, W
        # dx [ 0, 1, 0, -1]
        # dy [-1, 0, 1,  0]
        chars = []
        for dx,dy in zip([ 0, 1, 0, -1], [-1, 0, 1,  0]):
            if dx == 0 and dy == 0:
                continue
            nx = x+dx
            ny = y+dy
            if print_out:
                print(dx, dy, self.board[ny][nx])
            chars.append(self.board[ny][nx])
        return chars
    
    def print_out(self, path=None):
        for y in range(self.height):
            for x in range(self.width):            
                m = asciimap2 if path and x in path[y] else asciimap
                print(m.get(self.board[y][x], self.board[y][x]), end="")
            print()

def get_next_dir(cur_dir):
    if cur_dir == N:
        return E
    if cur_dir == E:
        return S
    if cur_dir == S:
        return W
    if cur_dir == W:
        return N

def get_right_dir(dir):
    if dir == N:
        return E
    if dir == E:
        return S
    if dir == S:
        return W
    if dir == W:
        return N

def get_left_dir(dir):
    if dir == N:
        return W
    if dir == E:
        return N
    if dir == S:
        return E
    if dir == W:
        return S
    
# follow the path, and look right & left, we count any thing right/left of the current direction
def count_left_and_right(c1, ch, dir, path, inside):
    directions_to_test = [get_right_dir(dir), get_left_dir(dir)]

    # corners count in two direcitons.
    if ch == "L":
        if dir == E:
            directions_to_test.append(get_right_dir(S))
            directions_to_test.append(get_left_dir(S))
        else:
            assert dir == N
            directions_to_test.append(get_right_dir(W))
            directions_to_test.append(get_left_dir(W))
    if ch == "F":
        if dir == E:
            directions_to_test.append(get_right_dir(N))
            directions_to_test.append(get_left_dir(N))
        else:
            assert dir == S
            directions_to_test.append(get_right_dir(W))
            directions_to_test.append(get_left_dir(W))
    if ch == "7":
        if dir == S:
            directions_to_test.append(get_right_dir(E))
            directions_to_test.append(get_left_dir(E))
        else:
            assert dir == W
            directions_to_test.append(get_right_dir(E))
            directions_to_test.append(get_left_dir(E))
    if ch == "J":
        if dir == N:
            directions_to_test.append(get_right_dir(E))
            directions_to_test.append(get_left_dir(E))
        else:
            assert dir == W
            directions_to_test.append(get_right_dir(S))
            directions_to_test.append(get_left_dir(S))


    for move in directions_to_test:
        while True:
            if move == N:
                c1 = (c1[0], c1[1] - 1)
            elif move == E:
                c1 = (c1[0]+1, c1[1])
            elif move == S:
                c1 = (c1[0], c1[1] + 1)
            elif move == W:
                c1 = (c1[0]-1, c1[1])
            else:
                assert False
            
            if c1[0] in path[c1[1]]:
                break

            inside.add(c1) 

def traverse(board, existing_path=None, inside=None):
    part1 = 0
    c1 = board.start
    path = defaultdict(list)
    path[c1[1]].append(c1[0])

    dir = board.find_starting_dir()
    Stop = False

    directed_path = defaultdict(list)
    directed_path[c1] = dir
    while not Stop:
        if existing_path:
            count_left_and_right(c1, board.get(*c1), dir, existing_path, inside)
        move = dir
        if move == N:
            c1 = (c1[0], c1[1] - 1)
        elif move == E:
            c1 = (c1[0]+1, c1[1])
        elif move == S:
            c1 = (c1[0], c1[1] + 1)
        elif move == W:
            c1 = (c1[0]-1, c1[1])
        else:
            assert False, move

        path[c1[1]].append(c1[0])
        directed_path[c1] = move

        # Check end condition, if we've looped we are done.
        if c1 == board.start:
            Stop = True
        else:
            # new position and direction
            ch = board.get(*c1)
            dir = m2[ch][dir]
            #print(c1)       
        part1 += 1
    return part1 // 2, path, directed_path


def run(file, render_answer=False):
    part1 = 0
    part2 = 0

    board = Board(file)
    #board.print_out()
    #print(board.start)

    part1, path, directed_path = traverse(board, None)
    answer(part1)

    inside = set()
    part1, path, _ = traverse(board, path, inside)
    answer(len(inside))

    # mark board
    if render_answer:
        for x,y in inside:
            board.set(x,y,"I")
        board.print_out()
        render(board.board, board.width, board.height, path)

    return part1, part2

if __name__ == "__main__":
    run("day10.txt", render_answer=True)