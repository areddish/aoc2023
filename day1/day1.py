from collections import defaultdict

reps = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    #"zero": "0"
}

part1 = 0
part2 = 0

with open("day1.txt") as file:
    for line in file.readlines():
        line = line.strip()

        part1_locations = []
        part2_locations = []

        for r in reps:
            idx = line.find(r, 0)
            while idx != -1:
                part2_locations.append((idx,reps[r]))
                idx = line.find(r, idx + 1)
        
        for i, ch in enumerate(line):
            if ch.isdigit(): # in "0123456789":
                part1_locations.append((i, ch))
                part2_locations.append((i, ch))
            
        part2_locations = list(sorted(part2_locations, key=lambda x:x[0]))

        part1 += int(part1_locations[0][1]) * 10+ int(part1_locations[-1][1])
        part2 += int(part2_locations[0][1]) * 10+ int(part2_locations[-1][1])

print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")