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

def render_board(galaxies,W,H):
    vs = list(galaxies.values())
    for y in range(H):
        for x in range(W):
            print("." if (x,y) not in vs else "#",end="")
        print()

def manhattan_distance(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def expand_galaxies(galaxies, offset, affected_cols, affected_rows):
    expanded_galaxy = {galaxy_num: galaxies[galaxy_num] for galaxy_num in galaxies}
    for y in reversed(affected_rows):
        for g in galaxies:
            if galaxies[g][1] > y:
                expanded_galaxy[g] = (expanded_galaxy[g][0], expanded_galaxy[g][1]+offset)

    for x in reversed(affected_cols):
        for g in galaxies:
            if galaxies[g][0] > x:
                expanded_galaxy[g] = (expanded_galaxy[g][0]+offset, expanded_galaxy[g][1])
    return expanded_galaxy

def compute_distances(galaxies):
    ans = 0
    for pair in pairs:
        a = galaxies[pair[0]]
        b = galaxies[pair[1]]
        #print(f"dist: {pair[0]} -> {pair[1]} = {man_dist(a,b)}")
        ans += manhattan_distance(a,b)
    return ans

galaxies = {}
rows_to_expand = []
columns_to_expand = []

W = 0
H = 0
#with open("test.txt") as file:
with open("day11.txt") as file:
    index = 1
    empty_col_tracker = None
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        W = len(line)
        if not empty_col_tracker:
            empty_col_tracker = [ch == "." for ch in line]
        row_is_empty = True
        for x,ch in enumerate(line):
            if ch == "#":
                galaxies[index] = (x,y)
                index += 1
                empty_col_tracker[x] = False
                row_is_empty = False
        if row_is_empty:
            rows_to_expand.append(y)
        H = y
H += 1

# Determine the empty columns
for x,v in enumerate(empty_col_tracker):
    if v:
        columns_to_expand.append(x)

# Generate the pairs of galaxies
pairs = set()
for id1 in galaxies.keys():
    for id2 in galaxies.keys():
        if id1 != id2 and (id2, id1) not in pairs:
            pairs.add((id1, id2))
#print(pairs, len(pairs))

# part 1
answer(compute_distances(expand_galaxies(galaxies, 1, columns_to_expand, rows_to_expand)))

# part 2
answer(compute_distances(expand_galaxies(galaxies, 1000000-1, columns_to_expand, rows_to_expand)))