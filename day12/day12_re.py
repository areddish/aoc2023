from itertools import permutations
from copy import copy
import sys
from functools import lru_cache
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

@lru_cache
def solve(s, groupings):
    # No more groups to find, and no more #'s
    if not groupings and "#" not in s:
        return 1
    
    # I we don't have any string left and we still have groups we've failed
    # or if we have string with #'s or ?'s and no groupings we also failed.
    if (not s and groupings) or (s and not groupings):
        return 0
    
    # leading .'s don't impact solution, but help with the memoization for
    # later problems, so just strip and solve
    if s[0] == ".":
        return solve(s[1:], groupings)

    # Wildcad, try both options    
    if s[0] == "?":
        return solve("." + s[1:], groupings) + solve("#" + s[1:], groupings) 

    # s[0] is a # -> try and form a group of #'s
    i = 0
    needed = groupings[0]
    while i < len(s) and s[i] == "#":
        i += 1
        needed -= 1

    # We have too many #'s in a row, fail.
    if needed < 0:
        return 0
    
    # We're at the end, if we have the right number we
    # are ok, otherwise fail
    if i == len(s):
        if needed == 0 and len(groupings) == 1:
            return 1
        return 0
    
    # first group cannot be formed, fail.
    if s[i] == ".":
        if needed != 0:
            return 0
        else:
            return solve(s[i:], groupings[1:])

    if s[i] == "?":
        if needed == 0:
            # it has to be a to create the group needed for the current
            # group
            return solve(s[i+1:], groupings[1:])
        return solve(s[:i] +"." + s[i+1:], groupings) + solve(s[:i] +"#" + s[i+1:], groupings) 

    # if we formed the group
    if needed == 0:
        return solve(s[i:], groupings[1:])


# assert solve("", [1,2]) == 0
# assert solve("##", []) == 0
# assert solve("#", [1]) == 1
# assert solve(".#", [1]) == 1
# assert solve("#.", [1]) == 1
# assert solve(".#.", [1]) == 1
# assert solve("?", [1]) == 1
# assert solve(".?", [1]) == 1
# assert solve("?.", [1]) == 1
# assert solve(".?.", [1]) == 1

# assert solve("???.###", [1,1,3]) == 1, solve("???.###", [1,1,3])
# assert solve(".??..??...?##.", [1,1,3]) == 4
# assert solve("?#?#?#?#?#?#?#?", [1,3,1,6]) == 1
# assert solve("????.#...#...", [4,1,1]) == 1 
# assert solve("????.######..#####.", [1,6,5]) == 4 
# assert solve("?###????????", [3,2,1]) == 10, solve("?###????????", [3,2,1])


part1 = 0
part2 = 0
#with open("test.txt") as file:
with open("day12.txt") as file:
    for y,line in enumerate(file.readlines()): 
        print("Processing #",y,end="")
        line = line.strip()
        # line = line.replace("....", ".")
        # line = line.replace("...", ".")
        # line = line.replace("..", ".") 
        springs, grouping = line.split()
        grouping = tuple([int(x) for x in grouping.split(",")])
#        springs, grouping = clean(springs, grouping)
#        print(springs, " Cleaned = ", springs)
        res1 = solve(springs, grouping)
        print(" p1 = ", res1)
        part1 += res1

        esprings = springs
        egroups = copy(grouping)
        for i in range(4):
            esprings += "?" + springs
            egroups += grouping
        part2 += solve(esprings, egroups)
answer(part1)
answer(part2)
