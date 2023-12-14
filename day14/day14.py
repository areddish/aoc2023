from collections import defaultdict
###
#   Submission helper, print the answer and copy it to the clipboard
#   to reduce the amount of times I have the answer and mistype it :).
###
import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

part1 = 0
part2 = 0

def print_board(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            print(board[y][x], end="")
        print()
    
def slide(board, x, y, dir, W, H):
    dx,dy = dir
    if dy != 0:
        while 0 <= y < H:
            y += dy
            if y < H and board[y][x] != ".":
                y -= dy
                break
        if y < 0:
            y = 0
        if y == H:
            y = H - 1
    if dx != 0:
        while 0 <= x < W:
            x += dx
            if x < W and board[y][x] != ".":
                x -= dx
                break
        if x < 0:
            x = 0
        if x == W:
            x = W - 1

    return (x,y)

def tilt(board, yrange, xrange, offset, W, H):
    for y in yrange:
        for x in xrange:
            if board[y][x] == "O":
                nx,ny = slide(board,x,y,offset, W, H)
                board[y][x] = "."
                board[ny][nx] = "O"

def compute_load(board, W, H):
    ans = 0
    for y in range(H):
        for x in range(W):
            if board[y][x] == "O":
                ans += H - y
    return ans

board = []

#with open("test.txt") as file:
with open("day14.txt") as file:
    index = 1
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        board.append(list(line))

    W = len(board[0])
    H = len(board)

    #print_board(board)
    answers = defaultdict(list)
    # This number found by testing
    #  1000 -> no answer
    #  5000 -> 3 answers (99862, 99861, 99875)
    #  8000 -> 2 answers (99861, 99875)
    #  10000 -> 1 answer.. and it's common with other's
    for i in range(1,10000+1):#000000+1):
        tilt(board, range(0,H), range(0,W), (0,-1), W, H)
        if i == 1:
            answer(compute_load(board, W, H))
            part1_done = True
        tilt(board, range(0,H), range(0,W), (-1,0), W, H)
        tilt(board, range(H-1,-1,-1), range(0,W), (0,1), W, H)
        tilt(board, range(0,H), range(W-1, -1, -1), (1,0), W, H)
        load = compute_load(board, W, H)
        answers[load].append(i)
        if i % 1000 == 0:
            print(f"Processed {i}")

    for k in answers:
        # need enough samples
        if len(answers[k]) < 100:
            continue
        # find the first occurence and the cycle
        index = min(answers[k])
        cycle = answers[k][-1] - answers[k][-2]
        #print(k, index, cycle)
        # if we could reach that in 1000000000, it's our answer.
        # could there by more than one?
        if (1000000000 - index) % cycle == 0:
            answer(k)            