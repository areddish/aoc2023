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
    print("Part 1 =" if answer_part == 1 else "Part 2 = ", v)
    answer_part = 2


part1 = 0
part2 = 0

def get_cubes(str):
    cubes = defaultdict(lambda: 0)
    parts = str.replace(";", "").replace(",", "").strip().split(" ")
    for x in range(0, len(parts), 2):
        num = int(parts[x])
        color = parts[x+1]
        cubes[color] = max(cubes[color], num)
    return cubes

#with open("test.txt") as file:
with open("day2.txt") as file:
    for line in file.readlines():
        parts = line.strip().split(":")
        game = int(parts[0].split()[1])
        cubes = get_cubes(parts[1])
        if cubes["red"] <= 12 and cubes["green"] <= 13 and cubes["blue"] <= 14:
            part1 += game
        part2 += cubes["red"] * cubes["blue"] * cubes["green"]
answer(part1)
answer(part2)