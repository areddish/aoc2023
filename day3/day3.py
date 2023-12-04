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

def get(board, x, y, w, h):
    if x < 0 or x >= w or y < 0 or y >= h:
        return None
    return board[y][x]

def has_symbol_near(board, x, y, w, h):
    result = False
    gear_location = None
    for dx, dy in [(-1,1), (0,1), (1,1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]:
        ch = get(board,x+dx,y+dy, w, h)
        if ch and not ch.isdigit() and ch != ".": #in "!@#$%^&*()_+-=":
            result = True
            gear_location = (x+dx, y+dy) if ch == "*" else None
    return result, gear_location

board = []
#with open("test.txt") as file:
with open("day3.txt") as file:
    for line in file.readlines():
        line = line.strip()
        board.append(list(line))

#numbers = []
numbers_near_symbols = []
gear_ratios = defaultdict(list)
h = len(board)
w = len(board[0])

for y in range(h):
    x = 0
    while x < w:
        num = ""
        is_near_symbol = False
        is_near_gear = None
        while x < w and board[y][x].isdigit():
            num += board[y][x]
            ns, ng = has_symbol_near(board, x, y, w, h)
            if not is_near_gear and ng:
                is_near_gear = ng
            is_near_symbol = is_near_symbol or ns
            x += 1
        if num != "":
            num = int(num)
            #numbers.append(num)
            ns, ng = has_symbol_near(board, x-1, y, w, h)
            is_near_gear = ng if ng else is_near_gear
            is_near_symbol = is_near_symbol or ns
            if is_near_gear:
                gear_ratios[is_near_gear].append(num)
            if is_near_symbol:
                numbers_near_symbols.append(num)
        x += 1

#print(numbers)
#print(gear_ratios)
for gear in gear_ratios:
    if len(gear_ratios[gear]) == 2:
        part2 += gear_ratios[gear][0] * gear_ratios[gear][1]

answer(sum(numbers_near_symbols))
answer(part2)